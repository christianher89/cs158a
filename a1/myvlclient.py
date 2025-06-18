from socket import *

serverName = '127.0.0.1'  # Replace with real server IP if needed
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

sentence = input("Write any sentence you want! (1-99 chars): ")
length = len(sentence)

if length < 1 or length > 99:
    print("Message must be between 1 and 99 characters.")
    clientSocket.close()
    exit()

# Prepare message: 2-byte length + message body
length_prefix = f"{length:02}"
message = (length_prefix + sentence).encode()
print(message)

# Meets the 64 bits restraint
for i in range(0, len(message), 64):
    clientSocket.send(message[i:i+64])

# Receives a response from myvlserver.py
received = b''
while len(received) < length:
    chunk = clientSocket.recv(64)
    if not chunk:
        break
    received += chunk

print("From server:", received.decode())
clientSocket.close()