CS158A Assignment 3 - Leader Election Algorithm
------------------------------------------------
This project implements the O(n²) leader election algorithm in an asynchronous ring topology using TCP sockets.

myleprocess.py is the distributed node program:

Uses TCP sockets and operates as both server and client with separate threads
Generates a unique UUID for each node using uuid.uuid4()
Listens on its own port (server) and connects to neighbor's port (client)
Implements leader election algorithm: forwards larger UUIDs, ignores smaller ones
When a node's UUID returns to itself, it declares itself as leader
Sends leader announcement with flag=1 around the ring for all nodes to learn
Logs all received, sent, and ignored messages to log.txt

HOW TO RUN THE PROGRAM:

1. Create three separate directories (node1, node2, node3)
2. Copy myleprocess.py to each directory
3. Create config.txt in each directory:

- Node1: 127.0.0.1,5001 and 127.0.0.1,5002
- Node2: 127.0.0.1,5002 and 127.0.0.1,5003
- Node3: 127.0.0.1,5003 and 127.0.0.1,5001

Run all three nodes simultaneously in separate terminals
Check log.txt files to see the algorithm execution

NOTES:
- All nodes must be started quickly to establish the ring topology
- The node with the highest UUID will be elected as leader
- Algorithm terminates when all nodes know the leader's identity
- Connection errors during termination are normal and expected
