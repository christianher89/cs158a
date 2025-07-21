import socket
import threading
import time
import uuid
import json
import sys

CONFIG_FILE = "config.txt"
LOG_FILE = None

# Message class for serialization
class Message:
    def __init__(self, uuid_val, flag):
        self.uuid = uuid_val
        self.flag = flag

    def to_json(self):
        return json.dumps({'uuid': str(self.uuid), 'flag': self.flag})

    @staticmethod
    def from_json(data):
        obj = json.loads(data)
        return Message(obj['uuid'], obj['flag'])

def write_log(message):
    with open(LOG_FILE, 'a') as f:
        f.write(message + '\n')
    print(message)


def load_config():
    with open(CONFIG_FILE, 'r') as f:
        lines = f.read().strip().split('\n')
        server_ip, server_port = lines[0].split(',')
        client_ip, client_port = lines[1].split(',')
        return (server_ip.strip(), int(server_port.strip())), (client_ip.strip(), int(client_port.strip()))


class LeaderElectionNode:
    def __init__(self, log_file):
        global LOG_FILE
        LOG_FILE = log_file

        open(LOG_FILE, 'w').close()

        self.my_addr, self.neighbor_addr = load_config()
        self.my_id = uuid.uuid4() 
        self.state = 0 
        self.leader_id = None 
        self.server_conn = None 
        self.client_conn = None 
        self.running = True
        self.initial_sent = False

        write_log(f"Node initialized with UUID: {self.my_id}")

    def start(self):
        # Start server thread
        t = threading.Thread(target=self.run_server)
        t.daemon = True
        t.start()

        time.sleep(1.5) 

        # Connect as client
        self.client_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connected = False
        while not connected and self.running:
            try:
                self.client_conn.connect(self.neighbor_addr)
                connected = True
                write_log("Outgoing connection established.")
            except:
                time.sleep(1)

        # Wait a bit more to see if we receive any messages first
        if connected:
            time.sleep(2)

            # Only send initial message if we haven't sent anything yet
            if not self.initial_sent and self.state == 0:
                init_msg = Message(self.my_id, 0)
                self.send_message(init_msg)
                self.initial_sent = True

            # Keep running until we know the leader
            while self.state == 0 and self.running:
                time.sleep(1)

            if self.leader_id:
                write_log(f"Leader is decided to {self.leader_id}")
                write_log("Election complete. Exiting.")

    def run_server(self):
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            server_sock.bind(self.my_addr)
            server_sock.listen(1)
            write_log(f"Server listening at {self.my_addr}")

            conn, addr = server_sock.accept()
            write_log(f"Accepted connection from {addr}")
            self.server_conn = conn

            # Use makefile for line-based reading
            f = conn.makefile()
            for line in f:
                if not self.running:
                    break
                try:
                    line = line.strip()
                    if not line:  # Skip empty lines
                        continue
                    msg = Message.from_json(line)
                    self.handle_message(msg)
                except json.JSONDecodeError:
                    continue
                except Exception as e:
                    break
            f.close()
        except Exception as e:
            if self.running:
                write_log(f"[INFO] Connection closed during shutdown")
        finally:
            try:
                if 'conn' in locals():
                    conn.close()
                server_sock.close()
            except:
                pass

    def send_message(self, msg):
        if not self.client_conn or not self.running:
            return

        try:
            self.client_conn.send((msg.to_json() + "\n").encode())
            write_log(f"Sent: uuid={msg.uuid}, flag={msg.flag}")
            self.initial_sent = True
        except Exception as e:
            if self.running:
                write_log(f"[ERROR] Send failed: {e}")

    # Handle incoming messages and implement leader election logic
    def handle_message(self, msg):
        # Convert string UUID back to UUID object for comparison
        msg_uuid = uuid.UUID(msg.uuid) if isinstance(msg.uuid, str) else msg.uuid

        # Compare incoming uuid with my_id to determine message relation
        if msg_uuid == self.my_id:
            cmp_result = "same"
        elif msg_uuid > self.my_id:
            cmp_result = "greater"
        else:
            cmp_result = "less"

        # Log the received message
        if self.state == 1:
            write_log(f"Received: uuid={msg.uuid}, flag={msg.flag}, {cmp_result}, 1")
            if self.leader_id:
                write_log(f"Current leader ID: {self.leader_id}")
        else:
            write_log(f"Received: uuid={msg.uuid}, flag={msg.flag}, {cmp_result}, 0")

        # Leader election decision making
        if msg.flag == 0:
            if self.state == 1:
                write_log(f"Ignored: uuid={msg.uuid}, flag={msg.flag}, leader already elected")
                return

            if msg_uuid == self.my_id:
                self.state = 1
                self.leader_id = self.my_id
                write_log(f"Leader is decided to {self.leader_id}")
                self.send_message(Message(self.leader_id, 1))
            elif msg_uuid > self.my_id:
                # Forward the larger UUID
                write_log(f"Forwarding larger UUID: {msg.uuid}")
                self.send_message(msg)
            else:
                # Ignore smaller UUIDs
                write_log(f"Ignored: uuid={msg.uuid}, flag={msg.flag}, smaller UUID")

        elif msg.flag == 1:
            if self.state == 0:
                # Accept the new leader
                self.state = 1
                self.leader_id = msg_uuid
                write_log(f"Leader is decided to {self.leader_id}")

                # Forward the announcement if it's not from me
                if msg_uuid != self.my_id:
                    self.send_message(msg)

                # Schedule termination
                threading.Timer(1.0, self.stop).start()
            else:
                if self.leader_id == msg_uuid:
                    # Leader announcement cycle complete
                    write_log(f"Leader announcement completed, terminating")
                    self.stop()
                else:
                    # Forward the message
                    self.send_message(msg)

    def stop(self):
        self.running = False
        try:
            if self.client_conn:
                self.client_conn.close()
        except:
            pass
        try:
            if self.server_conn:
                self.server_conn.close()
        except:
            pass


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python myleprocess.py <log_filename>")
        sys.exit(1)

    log_filename = sys.argv[1]

    try:
        node = LeaderElectionNode(log_filename)
        node.start()
    except KeyboardInterrupt:
        print("Process interrupted by user")
    except Exception as e:
        print(f"Error: {e}")
