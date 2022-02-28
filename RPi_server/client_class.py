import socket
from threading import *

class client(Thread):
    def __init__(self, host, port, message):
        Thread.__init__(self)
        self.host = host
        self.port = port
        self.message = message
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.start()
    def run(self):
        while True:
            if not self.connected:
                self.sock.connect((self.host, self.port))
                print("Client connected.")
                self.sock.sendall(self.message.encode())
                self.connected = True
            data = self.sock.recv(1024).decode()
            if data:
                print(data)


