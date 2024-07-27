import socket
import threading
import time

class LamportMulticastClient:
    def __init__(self, pid, server_port):
        self.pid = pid
        self.clock = 0
        self.server_port = server_port

    def send_message(self, event):
        self.clock += 1
        message = f"{self.pid}:{self.clock}:{event}"
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', self.server_port))
        client_socket.sendall(message.encode())
        client_socket.close()
        print(f"Client {self.pid} sent message: {message}")

    def simulate_events(self, num_events):
        for i in range(num_events):
            event = f"Event{i+1}"
            self.send_message(event)
            time.sleep(1)

def start_client(pid, server_port, num_events):
    client = LamportMulticastClient(pid, server_port)
    client.simulate_events(num_events)

if __name__ == "__main__":
    num_clients = 3
    server_port = 5002
    num_events = 6
    threads = []

    for pid in range(num_clients):
        t = threading.Thread(target=start_client, args=(pid, server_port, num_events))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()
