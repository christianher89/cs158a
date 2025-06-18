from socket import *

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

print("The server is ready to receive")

while True:
    connectionSocket, addr = serverSocket.accept()
    print(f"Connected from {addr[0]}")

    # Reads the 2-byte length prefix
    length_bytes = b''
    while len(length_bytes) < 2:
        chunk = connectionSocket.recv(2 - len(length_bytes))
        if not chunk:
            break
        length_bytes += chunk

    if not length_bytes:
        connectionSocket.close()
        continue

    msg_len = int(length_bytes.decode())
    print("msg_len:", msg_len)

    # Reads the rest of the message
    data = b''
    while len(data) < msg_len:
        chunk = connectionSocket.recv(min(64, msg_len - len(data)))
        if not chunk:
            break
        data += chunk

    sentence = data.decode()
    print("processed:", sentence)

    response = sentence.upper()
    print("msg_len_sent:", len(response))

    # Send the response with 64 bit restraint
    for i in range(0, len(response), 64):
        connectionSocket.send(response[i:i+64].encode())

    connectionSocket.close()
    print("Connection closed\n")