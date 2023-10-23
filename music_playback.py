import socket
import os
import threading
import wave
import pyaudio
import pickle
import struct
import sounddevice as sd
import soundfile as sf
import queue

# host_ip = socket.gethostbyname(socket.gethostname())
host_ip = "127.0.0.1"
port = 8080

class Playback_Thread(threading.Thread):
    def __init__(self, file_name):
        super().__init__()
        self.coordinates_queue = queue.Queue()
        self.file_name = file_name
    
    def playback(self):
        wf = wave.open(self.file_name, 'rb')
        framerate = 48000

        chunck_size = 1024

        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(2),
                    channels=2,
                    rate=framerate,
                    output=True,
                    frames_per_buffer=chunck_size)
        
        while True:
            packet = wf.readframes(chunck_size)

            if not self.coordinates_queue.empty():
                print("message: ", self.coordinates_queue.get())
                

            stream.write(packet)

def playback(file_name, q):
    wf = wave.open(file_name, 'rb')
    framerate = 48000

    chunck_size = 1024

    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(2),
                channels=2,
                rate=framerate,
                output=True,
                frames_per_buffer=chunck_size)
    
    while True:
        packet = wf.readframes(chunck_size)

        if not q.empty():
            print("message: ", q.get())
        
        stream.write(packet)


def recieve_stream():
    q = queue.Queue()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_address = (host_ip, port)
    server_socket.bind(socket_address)
    server_socket.listen(1)
    print(f"Listening on {host_ip}:{port}")

    client_socket, client_address = server_socket.accept() 
    print(f"Accepted connection from: {client_address}")


    file_name = client_socket.recv(1024).decode("utf-8")

    # playback_thread = Playback_Thread(file_name)
    playback_thread = threading.Thread(target=playback, args=(file_name, q, ))
    playback_thread.start()
    print('after playback start')

    
    while True:
        data = client_socket.recv(1024).decode("utf-8")
        q.put(data)
        
        if not data:
            break  # Break the loop if the connection is closed


    # Close the client and server sockets
    client_socket.close()
    server_socket.close()


    playback_thread.join()


def play_wav(file_path, duration_s):
    try:
        # Read the WAV file
        data, sample_rate = sf.read(file_path)
        sample_rate = 48000

        # Calculate the number of samples to play for the specified duration
        num_samples_to_play = int(duration_s * sample_rate)

        # Trim the audio data to the desired duration
        audio_data_to_play = data[:num_samples_to_play]

        # Play the audio data
        sd.play(audio_data_to_play, sample_rate)
        # sd.wait()  # Wait for the playback to finish

    except Exception as e:
        print(f"An error occurred: {e}")

# def play_wav_chunks(file_name):



    

if __name__ == "__main__":
    socket_thread = threading.Thread(target=recieve_stream)
    socket_thread.start()

    socket_thread.join()