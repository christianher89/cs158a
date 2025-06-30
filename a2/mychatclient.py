from socket import *
import threading
import sys

serverName = '127.0.0.1'
serverPort = 12345

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

print("Connected to chat server. Type 'exit' to leave.")

def receive():
    while True:
        try:
            message = clientSocket.recv(1024)
            if not message:
                break
            print(message.decode())
        except:
            break

def send():
    while True:
        msg = input()
        if msg.lower() == "exit":
            clientSocket.send(msg.encode())
            break
        clientSocket.send(msg.encode())
    clientSocket.close()
    print("Disconnected from server")
    sys.exit()

threading.Thread(target=receive, daemon=True).start()
send()
