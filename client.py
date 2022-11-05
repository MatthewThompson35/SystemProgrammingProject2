#!/usr/bin/env python3
"""Client for the server"""
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



CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
CLIENT.connect(ADDR)

def send(msg):
    """sends the message to the server"""
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    CLIENT.send(send_length)
    CLIENT.send(message)
    print(CLIENT.recv(2048).decode(FORMAT))


def get_input_for_channel():
    """Gets the input for the channel"""
    val = input("Enter the Channel you want to join from PY, QA, DB: ")
    while not check_channel_input(val):
        print("Channel not available!")
        val = input("Enter the Channel you want to join from PY, QA, DB: ")
    return val

def check_channel_input(val):
    """Checks if the input for channel is valid"""
    regex = re.compile("^(PY|QA|DB)$")
    if regex.match(val):
        return True
    return False

def close():
    """Closes the client"""
    CLIENT.close()

def main():
    """Main function"""
    val = get_input_for_channel()
    send(val)
    while val != DISCONNECT_MESSAGE:
        val = input("Message: ")
        send(val)



if __name__ == "__main__":
    main()
