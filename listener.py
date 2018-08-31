#!/usr/bin/env python
import socket
import signal
import subprocess

logPath="c:\cygwin64\home\Dave\KWH-Listener\listener.log"

def signal_handler(signal, frame):
    s.close()
    cs.close()
    exit(1)
signal.signal(signal.SIGINT, signal_handler)

# Logger
def log(logText):
    with open(logPath, "a") as log:
        log.write(logText)

# Logger
def unzip(path):
    zip_ref = zipfile.ZipFile(path, 'r')
    zip_ref.extractall(directory)
    zip_ref.close()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = ''
port = 11003

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
    
    # Close client connection
    cs.close()
    log("Client connection closed\n")
