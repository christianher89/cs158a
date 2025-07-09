import socket
import threading
import time
import uuid
import json
import sys

CONFIG_FILE = "config.txt"
LOG_FILE = "log.txt"

# Message class for serialization
class Message:
    def __init__(self, uuid_val, flag):
        self.uuid = str(uuid_val)
        self.flag = flag

    def to_json(self):
        return json.dumps({'uuid': self.uuid, 'flag': self.flag}) + "\n"

    @staticmethod
    def from_json(data):
        obj = json.loads(data)
        return Message(obj['uuid'], obj['flag'])

# This reads the config.txt file
def read_config():
    with open(CONFIG_FILE, 'r') as f:
        lines = f.read().strip().split('\n')
        my_ip, my_port = lines[0].split(',')
        neighbor_ip, neighbor_port = lines[1].split(',')
        return (my_ip.strip(), int(my_port.strip())), (neighbor_ip.strip(), int(neighbor_port.strip()))

def log(message):
    with open(LOG_FILE, 'a') as f:
        f.write(message + '\n')
    print(message)

class LeaderElectionNode:
    def __init__(self):
        self.uuid = uuid.uuid4()
        self.state = 0  # 0 is searching for leader, 1 means leader is known
        self.leader_id = None
        self.running = True
        self.lock = threading.Lock()

        self.server_conn = None
        self.client_conn = None

        # This clears the log file at start
        open(LOG_FILE, 'w').close()

        self.my_addr, self.neighbor_addr = read_config()
        log(f"Node initialized with UUID: {self.uuid}")

    def start(self):
        server_thread = threading.Thread(target=self.run_server)
        server_thread.daemon = True
        server_thread.start()

        # This gives the server time to start
        time.sleep(2)

        # Starts client connection and initial message
        self.run_client()

    def run_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            server_socket.bind(self.my_addr)
            server_socket.listen(1)
            log(f"[SERVER] Listening on {self.my_addr}")

            self.server_conn, addr = server_socket.accept()
            log(f"[SERVER] Connection accepted from {addr}")

            buffer = ""
            while self.running:
                try:
                    data = self.server_conn.recv(1024).decode()
                    if not data:
                        break

                    buffer += data
                    while "\n" in buffer:
                        msg_str, buffer = buffer.split("\n", 1)
                        if msg_str.strip():
                            msg = Message.from_json(msg_str)
                            self.handle_message(msg)

                except Exception as e:
                    log(f"[SERVER ERROR] {e}")
                    break

        except Exception as e:
            log(f"[SERVER BIND ERROR] {e}")
        finally:
            server_socket.close()

    def run_client(self):
        # Connects to neighbor
        connected = False
        while not connected and self.running:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect(self.neighbor_addr)
                self.client_conn = sock
                log(f"[CLIENT] Connected to {self.neighbor_addr}")
                connected = True
            except Exception as e:
                log(f"[CLIENT] Connection failed: {e}, retrying...")
                time.sleep(1)

        # Send initial message with own UUID
        if connected:
            initial_msg = Message(self.uuid, 0)
            self.send_message(initial_msg)

            while self.running:
                time.sleep(0.5)

    def handle_message(self, msg):
        with self.lock:
            msg_uuid = uuid.UUID(msg.uuid)

            if msg_uuid > self.uuid:
                comparison = "greater"
            elif msg_uuid == self.uuid:
                comparison = "same"
            else:
                comparison = "less"

            if self.state == 0:
                log(f"Received: uuid={msg.uuid}, flag={msg.flag}, {comparison}, {self.state}")
            else:
                log(f"Received: uuid={msg.uuid}, flag={msg.flag}, {comparison}, {self.state}")
                log(f"Current leader ID: {self.leader_id}")

            if msg.flag == 1:
                if self.state == 0:
                    self.leader_id = msg.uuid
                    self.state = 1
                    log(f"Leader is {self.leader_id}")
                    self.send_message(msg)
                    threading.Timer(1.0, self.terminate).start()
                else:
                    if self.leader_id == msg.uuid:
                        log(f"Leader announcement completed, terminating")
                        self.terminate()
                    else:
                        self.send_message(msg)
            else:
                if self.state == 1:
                    log(f"Ignored: uuid={msg.uuid}, flag={msg.flag}, leader already elected")
                    return

                if msg_uuid > self.uuid:
                    self.send_message(msg)
                elif msg_uuid == self.uuid:
                    log(f"Leader is decided to {self.uuid}")
                    self.leader_id = str(self.uuid)
                    self.state = 1
                    leader_msg = Message(self.uuid, 1)
                    self.send_message(leader_msg)
                    threading.Timer(2.0, self.terminate).start()
                else:
                    log(f"Ignored: uuid={msg.uuid}, flag={msg.flag}, smaller UUID")

    def terminate(self):
        self.running = False
        if self.leader_id:
            log(f"Final result: Leader is {self.leader_id}")

    def send_message(self, msg):
        try:
            if self.client_conn:
                self.client_conn.sendall(msg.to_json().encode())
                log(f"Sent: uuid={msg.uuid}, flag={msg.flag}")
        except Exception as e:
            log(f"[SEND ERROR] {e}")

if __name__ == "__main__":
    try:
        node = LeaderElectionNode()
        node.start()
    except KeyboardInterrupt:
        log("Process interrupted by user")
    except Exception as e:
        log(f"Error: {e}")