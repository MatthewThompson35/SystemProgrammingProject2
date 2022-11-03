#!/usr/bin/env python3
import socket
import threading

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "QUIT"
PYTHON = "PY"
SOFTWARE = "QA"
DATABASE = "DB"

python_notes = []
software_notes = []
database_notes = []
connected_channel = ""

sending = False

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
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
                conn.send("WHAT".encode(FORMAT))

            if msg == "WRIT":
                conn.send("YOU SAID WRIT".encode(FORMAT))
            if msg == "READ":
                conn.send("YOU SAID READ".encode(FORMAT))


            print(f"[{addr}] {msg}")


    conn.close()

def getMsg(conn):
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)
    return msg
def sendAllNotesInAssociatedChannel():
    if (connected_channel == "python"):
        for note in python_notes:
            conn.send(note.encode(FORMAT))
    if (connected_channel == "software"):
        for note in software_notes:
            conn.send(note.encode(FORMAT))
    if(connected_channel == "database"):
        for note in database_notes:
            conn.send(note.encode(FORMAT))

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
    print("[STARTING] server is starting...")
    start()

if __name__ == "__main__":
    main()
