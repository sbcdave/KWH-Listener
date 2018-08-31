#!/usr/bin/env python
import socket
import signal
import subprocess
import zipfile
from _thread import *
import threading

logPath="/KWH-Listener/logs/listener.log"

def signal_handler(signal, frame):
    s.close()
    cs.close()
    exit(1)
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
    while True:
        # data received from client
        data = c.recv(1024)
        if not data:
            print('Bye')
             
            # lock released on exit
            print_lock.release()
            break
 
        # Do stuff with data
 
        # send back to client
        c.send(data)
 
    # connection closed
    c.close()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = ''
port = 11001

try:
    s.bind((host, port))
except:
    log("Port "+str(port)+" in use\n")
    exit(1)
    
log("Listening...\n")

s.listen(1)

# Daemon listen on PORT for data
while True:
    # Waits for a command
    cs,addr = s.accept()

    # Beginning to process received command
    cmd = str(cs.recv(10))
    log("Received: "+cmd+"\n")

    # Pass data to parser
    #execfile("/KWH/datalogger/config/pyvars.py")
    #subprocess.Popen("/KWH/datalogger/transceive/ttyAMA0_setup.sh")
   
    # Send comfirmation back to datalogger
    cs.send(bytes("@888", "utf-8")) #KP standard - only used for backwards compatibility
    
    # Start a new thread and return its identifier
    start_new_thread(threaded, (c,))
    s.close()
    
    # Close client connection
    cs.close()
    log("Client connection closed\n")
s.close()

if __name__ == '__main__':
    Main()
