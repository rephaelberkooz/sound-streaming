import socket
import os
import threading
import wave
import pyaudio
import pickle
import struct
import sounddevice as sd
import soundfile as sf

# host_ip = socket.gethostbyname(socket.gethostname())
host_ip = "127.0.0.1"
port = 8080

def start_stream():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_address = (host_ip, port)
    server_socket.bind(socket_address)
    server_socket.listen(1)
    print(f"Listening on {host_ip}:{port}")

    client_socket, client_address = server_socket.accept() 
    print(f"Accepted connection from: {client_address}")

    file_path = client_socket.recv(1024).decode("utf-8")
    play_wav(file_path=file_path, duration_s=5)
    while True:
        data = client_socket.recv(1024).decode("utf-8")
        if not data:
            break  # Break the loop if the connection is closed
        print(f"Received: {data}")

    # file_path = "dreams.wav"

    # Close the client and server sockets
    client_socket.close()
    server_socket.close()


# C:\\Users\\Sam\\Documents\\Beat Saber\\Beat Saber\\Assets\\Beat Saber_Regular Intervals(slow)_Aespa Dreams Come True_PANNED.wav
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
        sd.wait()  # Wait for the playback to finish

    except Exception as e:
        print(f"An error occurred: {e}")



t1 = threading.Thread(target=start_stream, args=())
t1.start()
# play_wav("dreams.wav", 5)