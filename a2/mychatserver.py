from socket import *
import threading

serverPort = 12345
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen()

print(f"Server listening on 127.0.0.1:{serverPort}")

clients = []
lock = threading.Lock()

def broadcast(sender, message):
    with lock:
        for client in clients:
            if client != sender:
                try:
                    client.send(message)
                except:
                    clients.remove(client)

def handle_client(connectionSocket, addr):
    print(f"New connection from {addr}")
    while True:
        try:
            data = connectionSocket.recv(1024)
            if not data:
                break
            msg = data.decode()
            if msg.lower() == "exit":
                break
            full_message = f"{addr[1]}: {msg}".encode()
            broadcast(connectionSocket, full_message)
        except:
            break
    with lock:
        clients.remove(connectionSocket)
    connectionSocket.close()
    print(f"Disconnected from {addr}")

while True:
    connectionSocket, addr = serverSocket.accept()
    with lock:
        clients.append(connectionSocket)
    threading.Thread(target=handle_client, args=(connectionSocket, addr), daemon=True).start()
