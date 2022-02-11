# Multi connection client.
# It's very similar to the server, but instead of listening for connections, it starts by initiating connections via start_connections()
from select import select
import selectors
import socket
import types
import sys

sel = selectors.DefaultSelector()
messages = [b"Message 1 from client" , b"Message 2 from client."]

def start_connections(host, port, num_conns): #num_conns is number of connections to create to the server. Just like the server, each socket is set to non-blocking mode.
    server_addr = (host, port)
    for i in range(0, num_conns):
        connid = i + 1
        print("starting connection", connid, "to", server_addr)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(server_addr) #using this instead of connect() because connect would immediately raise a BlockingIOError exception.
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        data = types.SimpleNamespace(connid=connid, msg_total = sum(len(m) for m in messages), recv_total = 0, messages = list(messages), outb=b"")
        sel.register(sock, events, data=data)

def service_connection(key, mask):
    '''
    It's fundamentally the same as the server with one important difference. It keeps track of the number of bytes it's received from the server so it can close its side of the connection.
    When the server detects this, it closes its side of the connection too. Note that by doing this, the server depends on the client being well-behaved: the server expects the client
    to close its side of the connection when it's done sending messages. If the client doesn't close, the server will leave the connection open. In a real application, you may want to guard
    against this in your server and prevent client connections from accumulating if they don't send a request after a certain amount of time.
    
    '''
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024) #Should be ready to read
        if recv_data:
            print(f"Received {recv_data!r} from connection {data.connid}")
            data.recv_total += len(recv_data)
        if not recv_data or data.recv_total == data.msg_total:
            print(f"Closing connection {data.connid}")
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if not data.outb and data.messages:
            data.outb = data.messages.pop(0)
        if data.outb:
            print(f"Sending {data.outb!r} to connection {data.connid}")
            sent = sock.send(data.outb)  #Should be ready to write
            data.outb = data.outb[sent:]

if len(sys.argv) != 4:
    print(f"Usage: {sys.argv[0]} <host> <port> <num_connections>")
    sys.exit(1)

host, port, num_conns = sys.argv[1:4]
start_connections(host, int(port), int(num_conns))

try:
    while True:
        events = sel.select(timeout=1)
        if events:
            for key,mask in events:
                service_connection(key, mask)
        #Check for a socket being monitored to continue.
        if not sel.get_map():
            break
except KeyboardInterrupt:
    print("Keyboard interrupt, exiting.")
finally:
    sel.close()