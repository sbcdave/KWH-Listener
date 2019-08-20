#!/usr/bin/env python3
import socket
import signal
import subprocess
from _thread import *
import threading
import zlib
import sys

DEBUG = 1

def signal_handler(signal, frame):
    s.shutdown(socket.SHUT_RDWR)
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
    if DEBUG:
        print("in gzip")
    return str(zlib.decompress(data))

def check_and_parse(c):
    DEBUG = 0
    data = c.recv(300000)
    bytes_received = len(data)

    if DEBUG:
        print(data)

    STA = ""
    TIME = ""
    # If compressed un_gzip, else continue
    try:
        data = un_gzip(data)
        if DEBUG:
            print("un_gzip success")
            print(str(data))
    except:
        pass
    finally:
        # Confirm it's not spam before logging or responding
        try:
            parse1 = str(data).split("#")
            if parse1[1][:3] == "STA":
                # Check if it's a KWH Data Logger RTU
                password = parse1[0]
                parse2 = parse1[1].split(";")
                parse3 = []
                if DEBUG:
                    print("KWH Block about to split pairs")
                for pair in parse2:
                    # Grab STA station id variable
                    if pair.split(":")[0] == "STA":
                        STA = pair.split(":")[1]
                        if DEBUG:
                            print("STA: "+STA)
                    # Grab timestamp as variable
                    elif pair.split(":")[0] == "TM":
                        TIME = pair.split(":")[1]
                        if DEBUG:
                            print("TIME: "+TIME)
                    # Split out DISK data
                    elif pair.split(":")[0] == "DISK":
                        if DEBUG:
                           print("In DISK block")
                        value = pair.split(":")[1]
                        if DEBUG:
                           print("value: "+value)
                        DiskFREEkB = str(int(float(value)))
                        if DEBUG:
                           print("DiskFreekB: "+DiskFREEkB)
                        DiskPercentUsed = str(float(value)-int(DiskFREEkB))
                        if DEBUG:
                           print("DiskPercentUsed: "+DiskPercentUsed)
                        parse3.append(["DiskFREEkB", DiskFREEkB])
                        parse3.append(["DiskPercentUsed", DiskPercentUsed])
                    else:
                        parse3.append(pair.split(":"))
                # If we are here, it's likely a KWH Data Logger RTU
                # Check password against STA password file
                #if password <> :
                #    raise ValueError("Bad password")
            else:
                raise ValueError("SPAM")

            # If we made it to here the data seems legitimate
            # Send comfirmation back to datalogger
            c.send(bytes(TIME, "utf-8"))
            if DEBUG:
                log("Closing connection")
            c.shutdown(socket.SHUT_RDWR)
            c.close()

            # Calculate bytes received and compression efficiency
            uncompressed_bytes = len(data)
            compression_efficiency = 1.0 - (float(bytes_received)/float(uncompressed_bytes))
            log(str(bytes_received)+":"+str(uncompressed_bytes)+":"+str(compression_efficiency)+":"+str(data))

            # Add computed data to parse3 array for inserts into graphite
            parse3.append(["uncompressed_bytes", uncompressed_bytes])
            parse3.append(["bytes_received", bytes_received])
            parse3.append(["compression_efficiency", compression_efficiency])

            # Put in database
            import graphyte
            for item in parse3:
                graphyte.init('127.0.0.1', prefix=STA)
                graphyte.send(item[0], float(item[1]), timestamp=int(TIME))

                if DEBUG:
                    print("Send to Graphite complete")

        except ValueError as error:
            if error == "Bad password":
                log("BAD PASSWORD:"+str(data))
            # SPAM
        except Exception as error:
            log(str(error))
            print(error)
        except:
            pass

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
    if DEBUG:
        print("Starting a thread")
    start_new_thread(check_and_parse, (cs,))
