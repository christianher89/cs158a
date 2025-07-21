CS158A Assignment 3 - Leader Election Algorithm
--------------------------------------------------------------
This project implements the O(n²) leader election algorithm in an asynchronous ring topology using TCP sockets.

myleprocess.py is the distributed node program:

Uses TCP sockets and operates as both server and client with separate threads Generates a unique UUID for each node using uuid.uuid4() Listens on its own port (server) and connects to neighbor's port (client) Implements leader election algorithm: forwards larger UUIDs, ignores smaller ones When a node's UUID returns to itself, it declares itself as leader Sends leader announcement with flag=1 around the ring for all nodes to learn Logs all received, sent, and ignored messages to log.txt

HOW TO RUN THE PROGRAM

1. Place myleprocess.py and config.txt in your working directory
Configure and run first execution:

Edit config.txt to contain:
127.0.0.1,5001
127.0.0.1,5002

Run: python myleprocess.py log1.txt

Configure and run second execution:

Edit config.txt to contain:
127.0.0.1,5002
127.0.0.1,5003

Run: python myleprocess.py log2.txt

Configure and run third execution:

Edit config.txt to contain:
127.0.0.1,5003
127.0.0.1,5001

Run: python myleprocess.py log3.txt

Check the generated log files (log1.txt, log2.txt, log3.txt) to see the algorithm execution

Messages are logged with detailed information.
Example result message:

Node initialized with UUID: e759da97-6ece-4645-b108-e6dd5cd14c8c
Server listening at ('127.0.0.1', 5001)
Outgoing connection established.
Sent: uuid=e759da97-6ece-4645-b108-e6dd5cd14c8c, flag=0
Accepted connection from ('127.0.0.1', 53873)
Received: uuid=fe42402a-aa87-4d5f-b1dd-5ea842135986, flag=0, greater, 0
Sent: uuid=fe42402a-aa87-4d5f-b1dd-5ea842135986, flag=0
Received: uuid=fe42402a-aa87-4d5f-b1dd-5ea842135986, flag=1, greater, 0
Leader is decided to fe42402a-aa87-4d5f-b1dd-5ea842135986
Sent: uuid=fe42402a-aa87-4d5f-b1dd-5ea842135986, flag=1
Leader is decided to fe42402a-aa87-4d5f-b1dd-5ea842135986
Election complete. Exiting.

NOTES

Startup Timing: All nodes must be started quickly to establish the ring topology
Leader Selection: The node with the highest UUID will be elected as leader
Automatic Termination: Algorithm terminates gracefully when all nodes know the leader's identity
Connection Management: Clean shutdown prevents connection reset errors during termination
Error Recovery: Program handles network issues and malformed messages gracefully
State Consistency: Clear state transitions ensure reliable leader election process
