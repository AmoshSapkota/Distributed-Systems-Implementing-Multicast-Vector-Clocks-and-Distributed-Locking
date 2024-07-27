import threading
import time
from queue import PriorityQueue
import socket
import json

class VectorClockServer:
    def __init__(self, pid, port, num_processes):
        self.pid = pid
        self.vector_clock = [0] * num_processes
        self.num_processes = num_processes
        self.buffer = PriorityQueue()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(('localhost', port))
        self.server_socket.listen(5)
        print(f"Server {self.pid} started on port {port}")
        self.delivery_thread = threading.Thread(target=self.deliver_events)
        self.delivery_thread.start()

    def update_vector_clock(self, received_clock):
        for i in range(self.num_processes):
            self.vector_clock[i] = max(self.vector_clock[i], received_clock[i])

    def receive_message(self, conn, addr):
        try:
            data = conn.recv(1024).decode()
            if not data:
                return
            message = json.loads(data)
            event_id = message['event_id']
            received_clock = message['vector_clock']
            self.update_vector_clock(received_clock)
            self.buffer.put((received_clock, event_id))
            print(f"Server {self.pid}: Message received {event_id} with clock {received_clock}")
            self.deliver_events()
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Error decoding JSON from {addr}: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def deliver_events(self):
        while True:
            if self.buffer.empty():
                time.sleep(0.1)
                continue

            while not self.buffer.empty():
                received_clock, event_id = self.buffer.get()
                if self.can_deliver(received_clock):
                    print(f"Server {self.pid}: Delivered event {event_id}")
                    self.vector_clock[self.pid] += 1
                else:
                    self.buffer.put((received_clock, event_id))
                    break

    def can_deliver(self, received_clock):
        for i in range(self.num_processes):
            if i != self.pid and received_clock[i] > self.vector_clock[i]:
                return False
        return True

    def handle_client(self, client_socket):
        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            self.receive_message(client_socket, None)
        client_socket.close()

    def start_server(self):
        while True:
            print(f"Server {self.pid} is waiting for connections...")
            client_socket, address = self.server_socket.accept()
            print(f"Server {self.pid} accepted connection from {address}")
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

if __name__ == "__main__":
    num_processes = 3

    processes = []
    for pid in range(num_processes):
        port = 5002 + pid
        process = VectorClockServer(pid, port, num_processes)
        processes.append(process)

    threads = []
    for process in processes:
        t = threading.Thread(target=process.start_server)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()
