import socket
import os
import threading
import wave
import pickle
import struct
import sounddevice as sd
import soundfile as sf
import queue
import io
from scipy.io.wavfile import read, write
import numpy as np

# host_ip = socket.gethostbyname(socket.gethostname())
host_ip = "127.0.0.1"
port = 8080
framerate = 48000
chunck_size = 1024

def playback(file_name, q_messages):
    pass


def recieve_stream():
    # input_stream = pyaudio_input.open(format=pyaudio_input.get_format_from_width(quack.getsampwidth()),
    #     # using 1 channel here since we are using Mac microphone which
    #     # only has 1 channel input
    #     channels=1,
    #     rate=framerate,
    #     input=True,
    #     frames_per_buffer=chunck_size)
    

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_address = (host_ip, port)
    server_socket.bind(socket_address)
    server_socket.listen(1)
    print(f"Listening on {host_ip}:{port}")

    client_socket, client_address = server_socket.accept() 
    print(f"Accepted connection from: {client_address}")


    file_name = client_socket.recv(1024).decode("utf-8")
    q_messages = queue.Queue()

    # playback_thread = Playback_Thread(file_name)
    playback_thread = threading.Thread(target=playback, args=(file_name, q_messages, ))
    playback_thread.start()
    print('after playback start')

    
    while True:
        data = client_socket.recv(1024).decode("utf-8")
        q_messages.put(data)
        
        if not data:
            break  # Break the loop if the connection is closed


    # Close the client and server sockets
    client_socket.close()
    server_socket.close()


    playback_thread.join()
    

if __name__ == "__main__":
    socket_thread = threading.Thread(target=recieve_stream)
    socket_thread.start()

    socket_thread.join()