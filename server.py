import socket
from threading import Thread
from listenForClient import listen_for_client
from ipaddress import SERVER_HOST, SERVER_PORT, separater_token

# initializing set of all clients
client_sockets = set()

# creating a TCP socket
s = socket.socket()

# make the port as reusable port
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# binding the socket to the address we specified
s.bind((SERVER_HOST, SERVER_PORT))

# listen for upcoming connections
s.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

while True:
    # we keep listening for new connections all the time
    client_socket, client_address = s.accept()
    print(f"[+] {client_address} connected.")
    # add the new connected client to connected sockets
    client_sockets.add(client_socket)
    # start a new thread that listens for each client's messages
    t = Thread(target=listen_for_client, args=(client_socket,))
    # make the thread daemon so it ends whenever the main thread ends
    t.daemon = True
    # start the thread
    t.start()

# close client sockets
for cs in client_sockets:
    cs.close()
# close server socket
s.close()