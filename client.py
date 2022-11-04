#!/usr/bin/env python3
import socket
import re

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "QUIT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
PYTHON = "PY"
SOFTWARE = "QA"
DATABASE = "DB"

writing = False


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))


def getInputForChannel():
    val = input("Enter the Channel you want to join from PY, QA, DB: ")
    while not (checkChannelInput(val)):
        print("Channel not available!")
        val = input("Enter the Channel you want to join from PY, QA, DB: ")
    return val

def checkChannelInput(val):
    regex = re.compile("^(PY|QA|DB)$")
    if(regex.match(val)):
        return True
    return False


def main():
    val = getInputForChannel()
    send(val)
    while (val != DISCONNECT_MESSAGE):
        val = input("Message: ")
        send(val)


if __name__ == "__main__":
    main()
