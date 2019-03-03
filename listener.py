#!/usr/bin/env python3
import socket
import signal
import subprocess
import zipfile
from _thread import *
import threading

logPath="/KWH-Listener/listener.log"

def signal_handler(signal, frame):
    s.close()
    cs.close()
    exit()
signal.signal(signal.SIGINT, signal_handler)

# Logger
def log(logText):
    with open(logPath, "a") as log:
        log.write(logText)

# Unzipper
def unzip(path):
    zip_ref = zipfile.ZipFile(path, 'r')
    zip_ref.extractall(directory)
    zip_ref.close()

# thread fuction
def threaded(c):
    data = str(c.recv(50000))
    # Do stuff with data
    log(data)

    # Send comfirmation back to datalogger
    c.send(bytes("@888", "utf-8"))
    c.send(bytes(data, "utf-8"))

    # connection closed
    c.close()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = ''
port = 11003

try:
    s.bind((host, port))
except:
    log("Port "+str(port)+" in use\n")
    exit()

log("Listening...\n")

s.listen(1)

# Daemon listen on PORT for data
while True:
    # Waits for a command
    cs,addr = s.accept()

    # Start a new thread and return its identifier
    start_new_thread(threaded, (cs,))

if __name__ == '__main__':
    Main()
