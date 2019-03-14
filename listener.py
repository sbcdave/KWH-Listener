#!/usr/bin/env python3
import socket
import signal
import subprocess
from _thread import *
import threading
import zlib

def signal_handler(signal, frame):
    s.close()
    cs.close()
    exit()
signal.signal(signal.SIGINT, signal_handler)

logPath="/KWH-Listener/listener.log"
def log(textToLog):
    with open(logPath, "w") as log:
        log.write(textToLog)

def un_gzip(data):
    return str(zlib.decompress(data))

# thread fuction
def threaded(c):
    data = c.recv(300000)
    # Need logic for if compressed ..., else un_gzip
    data = un_gzip(data)

    # Need try catch to protect from spam
    log(data)
    data = data.split("#")
    password = data[0]
    data = data[1].split(";")
    for data_point in data:
        temp = data_point.split(":")
        key = temp[0]
        value = temp[1]
        print("key: "+key)
        print("value: "+value)


    # Send comfirmation back to datalogger
    # Might update to send back time stamp to help dataloggers
    # parallelize transmissions
    c.send(bytes("@888", "utf-8"))

    # connection closed
    c.close()


# listener setup
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

# listener listens on PORT for data. On receipt of data it passes 
# the data to a thread, and continues listening
while True:
    # Waits for a command
    cs,addr = s.accept()

    start_new_thread(threaded, (cs,))

if __name__ == '__main__':
    Main()
