#!/usr/bin/env python3
import socket
import signal
import subprocess
from _thread import *
import threading
import zlib
import sys

def signal_handler(signal, frame):
    s.close()
    cs.close()
    exit()
signal.signal(signal.SIGINT, signal_handler)

# Add logic to write to STA specific log file
logPath="/KWH-Listener/listener.log"
def log(textToLog):
    with open(logPath, "a") as log:
        log.write(textToLog+"\n")

def un_gzip(data):
    return str(zlib.decompress(data))

def check_and_parse(c):
    data = c.recv(300000)
    STA = ""
    TIME = ""
    # If compressed un_gzip, else continue
    try:
        data = un_gzip(data)
    except:
        pass
    finally:
        # Confirm it's not spam before logging or responding
        try:
            parse1 = str(data).split("#")
            # Check if it's a king pigeon
            if parse1[0] == "":
                # It looks like a king pigeon
                # Add KP parser code here later for backwards compatability
                log("No password: "+parse1[1])
            elif parse1[1][:3] == "STA":
                # Check if it's a KWH Data Logger RTU
                password = parse1[0]
                parse2 = parse1[1].split(";")
                parse3 = []
                for pair in parse2:
                    if pair.split(":")[0] == "STA":
                        STA = pair.split(":")[1]
                    elif pair.split(":")[0] == "TM":
                        TIME = pair.split(":")[1]
                    else:
                        parse3.append(pair.split(":"))
                # If we are here, it's likely a KWH Data Logger RTU
                # Check password against STA password file
                #if password <> :
                #    raise ValueError("Bad password")
            else:
                raise ValueError("SPAM")

            # If we made it to here the data seems legitimate
            log(str(data))

            # Send comfirmation back to datalogger
            c.send(bytes(TIME, "utf-8"))

            # Put in database
            db = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            db.connect(('127.0.0.1', 2003))

            for item in parse3:
                MESSAGE = STA+"."+item[0]+" "+item[1]+" "+TIME
                db.send(MESSAGE)
                rcv = s.recv(1024)
            s.close()

        except ValueError as error:
            if error == "Bad password":
                log("BAD PASSWORD:"+str(data))
            # SPAM
        except:
            pass
        finally:
            c.close()


# listener setup
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = ''
port = 11003

try:
    s.bind((host, port))
except:
    log("Port "+str(port)+" in use")
    exit()

log("Listening on "+str(port))

s.listen(1)

# listener listens on PORT for data. On receipt of data it passes 
# the data to a thread, and continues listening
while True:
    # Waits for a command
    cs,addr = s.accept()

    start_new_thread(check_and_parse, (cs,))

if __name__ == '__main__':
    Main()
