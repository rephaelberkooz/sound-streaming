# This is server code to send video and audio frames over TCP

import socket
import threading
import wave
import pyaudio
import pickle
import struct

# get the host's name and IP address
host_ip = socket.gethostbyname(socket.gethostname())
# define the port for communication
port = 8080

print('Host IP Address: ', host_ip)
print('Port: ', port)

# function for audio streaming
def audio_stream():
    # creates a socket for the server (enumerating defaults here)
    # AF_INET: IPv4 address family (designates type of addresses that socket can communicate)
    # SOCK_STREAM: TCP (type of socket)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host_ip, port))

    # enable server to accept connection, refuses new connections after 1 unaccepted connection
    server_socket.listen(0)

    CHUNK = 1024
    file_name = "../ln_Savanne.wav"

    wf = wave.open("ln_Savanne.wav", 'rb')
    framerate = wf.getframerate()

    print('{file_name} # channels: ', wf.getnchannels())
    print('{file_name} bitrate: ', framerate)
    
    # aquires system resources for PortAudio
    p = pyaudio.PyAudio()
    print('server listening at', (host_ip, port))
   
    # opens the input stream with the system mic
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    # using 1 channel here since we are using Mac microphone which
                    # only has 1 channel input
                    channels=1,
                    rate=framerate,
                    input=True,
                    frames_per_buffer=CHUNK)

    # accept a client connection
    client_socket, addr = server_socket.accept()
 
    # initialize data to be nothing
    data = None
    # while loop for running server
    while True:
        # if the client socket is accepted
        if client_socket:
            # i = 0
            while True:
                # read frames from the local file
                data = wf.readframes(CHUNK)

                # seriealize audio data
                a = pickle.dumps(data)

                # returns a bytes object packed to 'unsigned long long' format
                message = struct.pack("Q", len(a)) + a
                # if(i == 0):
                #     print(message)
                #     print(struct.pack("Q", len(a)))
                #     i += 1
                client_socket.sendall(message)
                
t1 = threading.Thread(target=audio_stream, args=())
t1.start()

