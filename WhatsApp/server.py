# chat_server.py

#	socket: This module allows your program to communicate over the network (TCP/IP)
# threading: This allows multiple clients to connect and communicate simultaneously, without freezing the server.
import socket
import threading


# HOST: The IP address the server will listen on.
# "127.0.0.1" means only the local computer can connect.
# If you want other computers on the same WiFi to connect,
# you’ll use the server’s actual IP (0.0.0.0 or 192.168.x.x).

# PORT: The network port the server will use. All clients must use the same port.
HOST = "127.0.0.1"   # localhost
PORT = 5555

# socket.socket(socket.AF_INET, socket.SOCK_STREAM): Creates a TCP/IP socket.
# AF_INET = IPv4
# SOCK_STREAM = TCP (reliable connection)
# server.bind((HOST, PORT)): Tells the server to listen on the IP/port you specified.
# server.listen(): Starts listening for incoming client connections.
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

# clients: List to store all connected client sockets.
# usernames: List to store the usernames of all connected clients.
# These lists are parallel: clients[i] corresponds to usernames[i].
clients = []
usernames = []

# broadcast is a helper function that sends a message to everyone connected.
# This is how messages from one user get delivered to all others.
def broadcast(message, sender_socket=None):
    """
    Improved broadcast:
    1. Optionally skips the sender (so you don't see your own msg twice).
    2. Handles encoding automatically.
    """
    if isinstance(message, str):
        message = message.encode("utf-8")

    for client in clients:
        if client != sender_socket:  # Don't send the message back to the person who wrote it
            try:
                client.send(message)
            except:
                # Clean up broken connections found during broadcast
                remove_client(client)

#	handle_client(client) handles one client in a separate thread.
# client.recv(1024): Receives up to 1024 bytes of data from that client.
# broadcast(message): Sends the received message to all other clients.
# If there is an error (client disconnects), we:
#	1.	Find the client’s index
#	2.	Remove them from clients and usernames lists
#	3.	Close the connection
#	4.	Inform everyone that the user left the chat
#	5.	Break the loop (stop the thread)
def handle_client(client):
    while True:
        try:
            message = client.recv(1024).decode("utf-8")

            # FEATURE: Private Messaging Logic
            # Syntax: /msg username message
            if message.startswith("/msg"):
                parts = message.split(" ", 2)
                target_user = parts[1]
                content = parts[2]

                if target_user in usernames:
                    target_index = usernames.index(target_user)
                    target_socket = clients[target_index]
                    target_socket.send(f"[PM from {usernames[clients.index(client)]}]: {content}".encode("utf-8"))
                else:
                    client.send("System: User not found.".encode("utf-8"))

            # FEATURE: Word Filtering (The "Family Friendly" Filter)
            elif "badword" in message.lower():
                client.send("System: Please keep the chat clean!".encode("utf-8"))

            else:
                broadcast(f"{message}", sender_socket=client)
        except:
            remove_client(client)
            break

# receive_connections() continuously waits for new clients.
# server.accept(): Pauses until a new client connects, returns a socket for that client and its address.
# client.send("USERNAME"): Asks the client to send its username.
# username = client.recv(1024).decode("utf-8"): Receives the username.
# Adds the client and username to the respective lists.
# Prints the username for server-side logs.
# broadcast(f"{username} joined the chat!"): Lets everyone know a new user joined.
# threading.Thread(target=handle_client, args=(client,)):
#                   Starts a new thread to handle messages from this client.
# This ensures the server can handle many clients at once without freezing.
#
def receive_connections():
    print("Server running...")

    while True:
        client, address = server.accept()
        print(f"Connected with {address}")

        client.send("USERNAME".encode("utf-8"))
        username = client.recv(1024).decode("utf-8")

        usernames.append(username)
        clients.append(client)

        print(f"Username is {username}")
        broadcast(f"{username} joined the chat!".encode("utf-8"))

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

#	Starts the server loop that waits for clients to connect.
# This is the main entry point of the server.
receive_connections()