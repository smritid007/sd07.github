import socket
import select

sockets = []

for port in range(10000,10002):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('127.0.0.1', port))
    sockets.append(server_socket)
print("sockets:", sockets)

empty = []
while True:
    readable, writable, exceptional = select.select(sockets, empty, sockets)
    print("inside while")
    for s in readable:
        print("inside readable")
        (client_data, client_address) = s.recv(1024)
        print("printing to check:",client_address, client_data)
        s.send(client_data, client_address)
for s in sockets:
   s.close()