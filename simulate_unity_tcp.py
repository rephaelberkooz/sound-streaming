import socket
import os
import threading
import pyaudio
import pickle
import struct
import random
import time

num_blocks = 10

# get the host's name and IP address
# host_ip = socket.gethostbyname(socket.gethostname())
host_ip = "127.0.0.1"
port = 8080

file_path = "ln_Savanne.wav"

def send_message_tcp(socket, data):
    message = data.encode()
    # serialized_data = pickle.dumps(data)
    # message = struct.pack("Q", len(serialized_data)) + serialized_data
    socket.sendall(message)

# create socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_address = (host_ip, port)
print('server listening at', socket_address)
client_socket.connect(socket_address) 
print("CLIENT CONNECTED TO", socket_address)

payload_size = struct.calcsize("Q")


send_message_tcp(client_socket, file_path)


for _ in range(num_blocks):
    coordinates = f'{[random.random()*20, random.random()*20, 15]}'

    time.sleep(1)
    send_message_tcp(client_socket, coordinates)
    print('sent', coordinates)

client_socket.close()
