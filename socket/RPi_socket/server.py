import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = socket.gethostname()
print(HOST)
PORT = 12345
s.bind((HOST, PORT))
s.settimeout(1.0)
s.listen()



try:
    while True:
        try:

                conn, addr = s.accept()
                print("Got connection from", addr)
                message = "Thank you for connecting."
                conn.send(message.encode())
                conn.close()
        except socket.timeout:
            pass
        except KeyboardInterrupt:
            pass
except KeyboardInterrupt:
    s.shutdown
    s.close()
    print("Server closed with KeyboardInterrupt!")

