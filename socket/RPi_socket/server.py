import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = socket.gethostname()
print(HOST)
PORT = 12345
s.bind((HOST, PORT))
s.listen()

while True:
    conn, addr = s.accept()
    print("Got connection from", addr)
    conn.send("Thank you for connecting.")
    conn.close()