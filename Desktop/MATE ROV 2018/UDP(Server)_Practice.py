import socket
import time

HOST='localhost'
PORT=5454


instance=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

while True:
    data=input("Enter a data\n").encode()
    instance.sendto(data,(HOST,PORT))
    print("Data has been sucessfully sent")
    time.sleep(1)
