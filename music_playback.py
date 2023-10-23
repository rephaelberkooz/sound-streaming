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
            
            if not self.coordinates_queue.empty():
                print("message: ", self.coordinates_queue.get())
               

            stream.write(packet)

def recieve_stream():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_address = (host_ip, port)
    server_socket.bind(socket_address)
    server_socket.listen(1)
    print(f"Listening on {host_ip}:{port}")

    client_socket, client_address = server_socket.accept() 
    print(f"Accepted connection from: {client_address}")

    # Assuming the first packet contains the filename for music playback
    file_path = client_socket.recv(1024).decode("utf-8")
    # play_wav(file_path=file_path, duration_s=5)
    wf = wave.open(file_path, 'rb')
    framerate = 48000

    chunck_size = 1024

    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(2),
                channels=2,
                rate=48000,
                output=True,
                frames_per_buffer=chunck_size)
    
    while True:
        data = client_socket.recv(1024).decode("utf-8")
        packet = wf.readframes(chunck_size)
        stream.write(packet)
        
        if not data:
            break  # Break the loop if the connection is closed
        print(f"Received: {data}")


    # Close the client and server sockets
    client_socket.close()
    server_socket.close()


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
    playback_thread = Playback_Thread("ln_Savanne.wav")
    playback_thread.start()
    playback_thread.join()

    # t1 = threading.Thread(target=recieve_stream, args=())
    # t1.start()
    # play_wav("dreams.wav", 5)
    # t1.join()