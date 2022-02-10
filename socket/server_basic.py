import socket

s = socket.socket() #Create a socket object
print("Socket successfully created")

# reserve a port on your computer, it can be anything
port = 12345

# Next bind to the port, we have not typed any ip in the ip field, instead we have inputted an empty string
# This makes the server listen to requests coming from other computers on the network

s.bind(("", port))
print("Socket binded to %s" %(port))

#Put the socket into listening mode
s.listen(5)
print("Socket is listening")

# A forever loop until we interrupt it or an error occurs
while True:
    # Establish a connection with client.
    c, addr = s.accept()
    print("Got connection from", addr)
    
    # send a thank you message to client. encoding to send byte type.
    c.send("Thank you for connecting".encode())
    
    #Close the connection with the client
    c.close()

    break # breaking once connection closed

# we made a socket object and reserved a port on our pc. After that, we bound our server to the specified port. Passing an empty string means that
# the server can listen to incoming connections from other computers as well. If we would have passed 127.0.0.1 then it would have listened to only those calls
# made within the local computer. After that we put the server into listening mode. 5 here means that 5 connections are kpt waiting if the server is busy 
# and if a 6th socket tries to connect then the connection is refused. At last, we make a while loop and start to accept all incoming connections and close 
# those connections after a thatnk you message to all connected sockets.
