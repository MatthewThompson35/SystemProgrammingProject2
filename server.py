#!/usr/bin/env python3
"""Server module. For testing Set TESTING to True"""
import socket
import threading
import logging

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "QUIT"
PYTHON = "PY"
SOFTWARE = "QA"
DATABASE = "DB"


PYTHON_NOTES = []
SOFTWARE_NOTES = []
DATABASE_NOTES = []

TESTING = True

SERV = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERV.bind(ADDR)
LOCK = threading.Lock()



def handle_client(conn, addr):

    """ Handles all of the mesages that the client sends to the server"""
    print(f"[NEW CONNECTION] {addr} connected.")
    ip_address = str(addr[0])
    logging.info("Client connected at: %s", ip_address)
    connected_channel = ""
    connected = True
    writing = False
    while connected:
        if TESTING:
            msg = DISCONNECT_MESSAGE
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
        logging.info("Message sent by %s -- %s", addr, msg)
        if msg == DISCONNECT_MESSAGE:
            connected = False
        elif msg in (PYTHON, SOFTWARE, DATABASE, DISCONNECT_MESSAGE):
            if msg == PYTHON:
                connected_channel = "python"
            if msg == SOFTWARE:
                connected_channel = "software"
            if msg == DATABASE:
                connected_channel = "database"
        elif writing:
            LOCK.acquire()
            writing = add_notes_to_channel(connected_channel, msg, addr)
            LOCK.release()

        elif msg == "WRIT":
            writing = True
        elif msg == "READ":
            conn.send(get_all_notes_to_string(connected_channel).encode(FORMAT))
        get_ending(msg, conn)
        print(f"[{addr}] {msg}")

    logging.info("Client disconnected at: %s", ip_address)
    conn.close()

def get_ending(msg, conn):
    """gets the ending message"""
    if msg == "WRIT":
        conn.send("SEND".encode(FORMAT))
    else:
        conn.send("WHAT".encode(FORMAT))
def add_notes_to_channel(connected_channel, msg, addr):
    """Adds notes to the specified channel"""
    if connected_channel == "python":
        result = str(addr)
        result += " " + msg
        PYTHON_NOTES.append(result)
    if connected_channel == "software":
        result = str(addr)
        result += " " + msg
        SOFTWARE_NOTES.append(result)
    if connected_channel == "database":
        result = str(addr)
        result += " " + msg
        DATABASE_NOTES.append(result)
    return False

def get_all_notes_to_string(connected_channel):
    """Gets all of the notes that are in the correlated channel """
    if connected_channel == "python":
        result = '\n'.join(PYTHON_NOTES)
    if connected_channel == "software":
        result = '\n'.join(SOFTWARE_NOTES)
    if connected_channel == "database":
        result = '\n'.join(DATABASE_NOTES)
    return result + "\n"

def start():
    """Starts the server"""
    SERV.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = SERV.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")



def main():
    """The main function"""
    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', filename='serverlog.log', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
    print("[STARTING] server is starting...")
    start()

if __name__ == "__main__":
    main()
