# Socket programming is a way of connecting two nodes on a network to communicate with each other. One socket (node) listens on a particular port at an 
# IP, while the other socket reaches out to the other to form a connection. The server forms the listener socket while the client reaches out to the server.
# There is a server and a client.

import socket
import sys
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as err:
    print("socket creation failed with error %s" %(err))

# here we made a socket instance and passed two parameters. AF_INET refers to the address-family ipv4. SOCK_STREAM means connection-oriented TCP protocol.
# Transmission Control Protocol (TCP) is a transport protocol that is used on top of IP to ensure reliable transmission of packets. Now we can connect to a server using this
# socket. We can only connect to a server by knowing its IP.
try:
    ip = socket.gethostbyname("www.google.com")
except socket.gaierror:
    print("there was an error resolving the host")
    sys.exit()


# An example script to connect to Google using socket programming

port = 80
# both socket and port are the terms used in Transport Layer. A port is a logical construct assigned to network processes so that they can be identified within the system.
# a socket is a combination of port and IP address. Port is the number used by particular software.

# connecting to the server
s.connect((ip, port))
print("The socket has successfully connected to google")

