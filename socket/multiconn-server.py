import selectors # A selector object provides methods for specifying waht events to look for on a socket, and then lets the caller wait for events in a platform-independent way
import socket
import types
import sys

sel = selectors.DefaultSelector()






def accept_wrapper(sock):
    conn, addr = sock.accept()  #Should be ready to read
    print("accepted connection from", addr)
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"") #We create an object to hold the data we want included along with the socket using the class.
    events = selectors.EVENT_READ | selectors.EVENT_WRITE #We want to know when the client connection is ready for reading and writing
    sel.register(conn, events, data=data) #The events mask, socket and data objects are passed to sel.register()

def service_connection(key, mask): # Hearth of the simple multi-connection server. key is the namedtuple returned from select()
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ: # If the socket is ready for reading, then this is true and sock.recv() is called. Any data that's read is appended to data.outb so it can be sent later.
        recv_data = sock.recv(1024) #Should be ready to read
        if recv_data:
            data.outb += recv_data
        else:
            print("closing connection to", data.addr)
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE: #When the socket is ready for writing, whşch should always be the case for a healthy socket, any received data stored in data.outb is echoes to the client
        if data.outb:
            print("echoing", repr(data.outb), "to", data.addr)
            sent = sock.send(data.outb) #Should be ready to write
            data.outb = data.outb[sent:]
if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} <host> <port>")
    sys.exit(1)
host, port = sys.argv[1], int(sys.argv[2])
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
print("listening on", (host, port))
lsock.setblocking(False) #With this, calls made to this socket will no longer block. A socket function or method that temporarily suspends your application is a blocking call
sel.register(lsock, selectors.EVENT_READ, data=None) #Registers the socket to be monitored with sel.select() for the events you're interested in.

#Data is used to store whatever arbitrary data you'd like along with the socket. It's returned when select() returns. We'll use data to keep track of what
#is been sent and received on the socket.



#Event loop
try:
    while True:
        events = sel.select(timeout=None) #Blocks until there are sockets ready for I/O. it returns a list of (key,events) tuples, one for each socket.
        for key, mask in events:
            if key.data is None: #Then we know it's from the listening socket and we need to accept() the connection
                accept_wrapper(key.fileobj)
            else: #Then we know it's a client socket that's already been accepted and we need to service it.
                service_connection(key, mask)
except KeyboardInterrupt:
    print("Keyboard interrupted, exiting.")
finally:
    sel.close()
