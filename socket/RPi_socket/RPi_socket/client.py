import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = "DESKTOP-C6F9ATQ"
PORT = 12345

s.connect((HOST, PORT))
print(s.recv(1024))
s.close()