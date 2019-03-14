#!/usr/bin/env python3
import socket
import signal
import subprocess
import zipfile
from _thread import *
import threading
import zlib

logPath="/KWH-Listener/listener.log"

def signal_handler(signal, frame):
    s.close()
    cs.close()
    exit()
signal.signal(signal.SIGINT, signal_handler)

# Loggers
def logtext(textToLog):
    with open(logPath, "w") as log:
        log.write(textToLog)
def logbytes(bytesToLog):
    with open(logPath, "wb") as log:
        log.write(bytesToLog)

# Unzipper
def unzip(path):
    zip_ref = zipfile.ZipFile(path, 'r')
    zip_ref.extractall(directory)
    zip_ref.close()

# thread fuction
def threaded(c):
    data = c.recv(300000)
    # Do stuff with data
    logbytes(data)

    # Send comfirmation back to datalogger
    c.send(bytes("@888", "utf-8"))
    c.send(data)

    # connection closed
    c.close()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = ''
port = 11003

try:
    s.bind((host, port))
except:
    logtext("Port "+str(port)+" in use\n")
    exit()

logtext("Listening...\n")

s.listen(1)

# Daemon listen on PORT for data
while True:
    # Waits for a command
    cs,addr = s.accept()

    # Start a new thread and return its identifier
    start_new_thread(threaded, (cs,))

if __name__ == '__main__':
    Main()
