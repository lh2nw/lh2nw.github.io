# chat_client.py

# Allows the program to communicate over network connections (TCP/IP). Needed to connect to the chat server
# Allows running multiple tasks simultaneously. Since we want to send and receive at the same time!
import socket
import threading
from datetime import datetime # For timestamps

#	HOST = server IP address.
# 127.0.0.1 means connect to server running on same machine.
# PORT = communication channel number.
# Must match server settings.
HOST = "127.0.0.1"
PORT = 5555

username = input("Choose your username: ")

# Creates a TCP socket.
# AF_INET = IPv4.
# SOCK_STREAM = TCP (reliable connection).
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#	Establishes connection to chat server.
#	If server is not running → connection fails.
client.connect((HOST, PORT))

#	Defines function responsible for listening to server messages.
def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            if message == "USERNAME":
                client.send(username.encode("utf-8"))
            else:
                # Add a timestamp to incoming messages
                time_now = datetime.now().strftime("%H:%M")
                print(f"[{time_now}] {message}")
        except:
            print("\n[!] Lost connection to server.")
            break


def write_messages():
    while True:
        msg = input("")

        # FEATURE: Simple Slash Commands
        if msg.startswith("/"):
            if msg == "/quit":
                client.close()
                break
            elif msg == "/help":
                print("Commands: /quit, /help, /shout")
                continue
            elif msg.startswith("/shout "):
                msg = msg.replace("/shout ", "").upper() + "!! 🔊"

        message = f"{username}: {msg}"
        client.send(message.encode("utf-8"))

threading.Thread(target=receive_messages).start() # Start background thread for receiving messages. Allows messages to appear while user types.
threading.Thread(target=write_messages).start() # Start another thread for sending messages.