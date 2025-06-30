CS158A Assignment 2 - Multi-Client Chat Server
----------------------------------------------

This project includes a server and a client program that use TCP sockets to create a simple real-time chat system.

mychatserver.py is the server program:
- Uses TCP sockets and listens on port 12345.
- Accepts multiple clients and handles each with a separate thread.
- Maintains a list of active clients.
- When a client sends a message, the server relays it to all **other** connected clients.
- Message format sent to clients: "{port_number}: {message}".
- Prints client connections and disconnections to the server console.

mychatclient.py is the client program:
- Connects to the server at 127.0.0.1:12345 using TCP.
- Runs two threads: one for sending messages and one for receiving.
- Allows the user to type and send messages at any time.
- Automatically displays messages from other clients.
- Disconnects cleanly when the user types `exit`.

HOW TO RUN THE PROGRAM:
1. Run `mychatserver.py` first in a terminal or IDE.
2. In separate terminals, run one or more instances of `mychatclient.py`.
3. Type a message and press Enter to send it. You will see messages from others.
4. Type `exit` to leave the chat.

NOTES:
- Server must be running before clients can connect.
- Only other clients will receive your messages (you won’t see your own).
- All communication uses a 1024-byte buffer and TCP, as required by the assignment.
