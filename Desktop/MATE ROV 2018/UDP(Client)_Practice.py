import socket

HOST='localhost'
PORT=8000

instance=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
instance.bind((HOST,PORT))

while True:
    msg=instance.recv(40).decode()
    print(msg)
