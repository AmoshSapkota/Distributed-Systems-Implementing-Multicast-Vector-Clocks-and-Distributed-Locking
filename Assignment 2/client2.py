import socket
import threading
import time
import json

class VectorClockClient:
    def __init__(self, pid, server_ports, num_processes):
        self.pid = pid
        self.vector_clock = [0] * num_processes
        self.server_ports = server_ports

    def increment_clock(self):
        self.vector_clock[self.pid] += 1

    def send_message(self, event):
        self.increment_clock()
        message = {
            'event_id': f"{self.pid}.{self.vector_clock[self.pid]}",
            'vector_clock': self.vector_clock.copy()  # Make sure to send a copy of the clock
        }
        for port in self.server_ports:
            self._send_message_to_port(port, message)
        print(f"Client {self.pid} sent message: {message}")

    def _send_message_to_port(self, port, message):
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(('localhost', port))
            client_socket.sendall(json.dumps(message).encode())
            client_socket.close()
        except Exception as e:
            print(f"Error sending message to port {port}: {e}")

    def simulate_events(self, num_events):
        for i in range(num_events):
            event = f"Event{i+1}"
            self.send_message(event)
            time.sleep(1)

def start_client(pid, server_ports, num_events, num_processes):
    client = VectorClockClient(pid, server_ports, num_processes)
    client.simulate_events(num_events)

if __name__ == "__main__":
    num_clients = 3
    base_port = 5002
    num_events = 6
    num_processes = 3
    threads = []

    for pid in range(num_clients):
        server_ports = [base_port + i for i in range(num_clients) if i != pid]
        t = threading.Thread(target=start_client, args=(pid, server_ports, num_events, num_processes))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()
