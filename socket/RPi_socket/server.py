import socket
import threading
import time
import os
import errno




try:
    from signal import signal, SIGPIPE, SIG_DFL
    signal(SIGPIPE, SIG_DFL)
except ImportError:  # If SIGPIPE is not available (win32), we don't have to do anything to ignore it
    pass




serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
HOST = socket.gethostname()
LOCAL_IP = socket.gethostbyname(HOST)

serversocket.listen()
print("Server started and listening")

while True:
    try:
        clientsocket, address = serversocket.accept()
    except socket.timeout:
        pass
    except socket.error as e:
        if isinstance(e.args, tuple):
            print("errno is %d" %e[0])
            if e[0] == errno.EPIPE: 
                print("Detected remote disconnect")
            else:
                pass
        else:
            print("Socket error", e)
    except KeyboardInterrupt:
        serversocket.shutdown()
        serversocket.close()
        print("Server closed via KeyboardInterrupt")
        break






