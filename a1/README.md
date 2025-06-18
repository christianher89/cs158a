CS158A Assignment 1 - Variable Length Message

myvlclient.py is the client program:
- Holds a default server name and server port (server name/IP can be changed if need)
- Prompts the user for a message.
- Automatically prefixes the user's message with a 2-digit length of the message.
- Sends the message to the server (myvlserver.py).
- It receives the message in uppercase.

myvlserver.py is the server program:
- Holds the default server port 12000.
- Prints a message saying that server is ready and waits for incoming clients
- Once connected, it reads the first 2 bytes of the message length
- Reads the rest of the message
- Converts message in uppercase and sends back to the client.

HOW TO RUN THE PROGRAM:
1. Run the myvlserver.py program first through an IDE or command prompt/terminal.
2. Run the myvlclient.py program.
3. Type in any sentence.

![Server connection](https://github.com/user-attachments/assets/5077306e-a9a2-45a0-a21a-059307d661b4)
![Client connection](https://github.com/user-attachments/assets/e7490c4b-f4d2-42e8-a39f-e174db3881f5)
