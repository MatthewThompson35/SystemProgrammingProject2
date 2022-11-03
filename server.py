#!/usr/bin/env python3
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


python_notes = ["Testing read", "Work"]
software_notes = ["SOFTWARE", "notes"]
database_notes = ["database", "notes"]

sending = False

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    logging.info("Client connected at: " + addr[0])
    connected_channel = ""
    connected = True
    writing = False
    while connected:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
            if msg in (PYTHON,SOFTWARE,DATABASE,DISCONNECT_MESSAGE):
                if msg == PYTHON:
                    connected_channel = "python"
                if msg == SOFTWARE:
                    connected_channel = "software"
                if msg == DATABASE:
                    connected_channel = "database"

            if(writing == True):
                if (connected_channel == "python"):
                    python_notes.append(msg)
                if (connected_channel == "software"):
                    software_notes.append(msg)
                if(connected_channel == "database"):
                    database_notes.append(msg)
                writing = False

            if msg == "WRIT":
                writing = True

            if msg == "READ":
                conn.send(getAllNotesToString(connected_channel).encode(FORMAT))

            conn.send("WHAT".encode(FORMAT))
            print(f"[{addr}] {msg}")


    conn.close()

def getAllNotesToString(connected_channel):
    result = ""
    if (connected_channel == "python"):
        result = '\n'.join(python_notes)
    if (connected_channel == "software"):
        result = '\n'.join(software_notes)
    if(connected_channel == "database"):
        result = '\n'.join(database_notes)
    return result + "\n"

def addNoteToAssociatedChannel(msg):
    if (connected_channel == "python"):
        python_notes.append(msg)
    if (connected_channel == "software"):
        software_notes.append(msg)
    if(connected_channel == "database"):
        database_notes.append(msg)

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

def main():
    logging.basicConfig(filename='serverlog.log', level=logging.INFO)
    print("[STARTING] server is starting...")
    start()

if __name__ == "__main__":
    main()
