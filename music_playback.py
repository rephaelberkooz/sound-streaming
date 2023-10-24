import ast
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
import io
from scipy.io.wavfile import read, write
import numpy as np
import mido
import random
import sys
import time
from mido import Message

# host_ip = socket.gethostbyname(socket.gethostname())
host_ip = "127.0.0.1"
port = 8080
framerate = 48000
chunck_size = 1024

def print_ports(heading, port_names):
    print(heading)
    for name in port_names:
        print(f"    '{name}'")
    print()

def playback(file_name, q_messages):
    # # instantiating the queue of quack chucks
    # q_quack = queue.Queue()
    # # using a quack sound for testing
    # quack = wave.open('quack48.wav', 'rb')
    # # print(quack.getframerate())
    # while True:
    #     chunck = quack.readframes(chunck_size)
    #     if not chunck:
    #         break
    #     q_quack.put(chunck)
    
    # opening the file name sent by the server
    wf = wave.open(file_name, 'rb')

    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(2),
                channels=2,
                rate=framerate,
                output=True,
                frames_per_buffer=chunck_size)
    
    while True:
        song_packet = wf.readframes(chunck_size)
        # What I'd like to do here is convert the song_packet and the quack numpy arrays, and add them together to mix the sound
        # if not q_quack.empty():
            # song_numpy = np.frombuffer(packet, dtype="int16") * 0.5
            # quack_numpy = np.frombuffer(quack.get(), dtype="int16") * 0.5
            # mixed_sounds = song_numpy + quack_numpy
            # buffer = io.BytesIO()
            # write(buffer, framerate, mixed_sounds)
            # stream.write(buffer.read())
        # else:

        stream.write(song_packet)


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
    # playback_thread = threading.Thread(target=playback, args=(file_name, q_messages, ))
    # playback_thread.start()
    # print('after playback start')

    
    # notes = [0, 32, 64, 92]
    map_dict = {0: [0,0], 1: [127,0], 2: [0,127], 3: [127,127]}
    try:
        with mido.open_output('loopMIDI Port 2', autoreset=True) as midi_port:
            while True:
                data = client_socket.recv(1024).decode("utf-8")
                int_value = ast.literal_eval(data)
                print('here is the float', int_value)

                on = Message('control_change', value=map_dict[int_value][0], channel=1, control=0)
                on2 = Message('control_change', value=map_dict[int_value][1], channel=2, control=1)
                # print(f'Sending {on, on2}')
                midi_port.send(on)
                midi_port.send(on2)
                
                if not data:
                        break  # Break the loop if the connection is closed
    except KeyboardInterrupt:
        pass

    # Close the client and server sockets
    client_socket.close()
    server_socket.close()


    # playback_thread.join()
    

if __name__ == "__main__":
    socket_thread = threading.Thread(target=recieve_stream)
    socket_thread.start()

    socket_thread.join()