import threading
import time
from queue import PriorityQueue
import socket

class LamportMulticastServer:
    def __init__(self, pid, port):
        self.pid = pid
        self.clock = 0
        self.buffer = PriorityQueue()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(('localhost', port))
        self.server_socket.listen(5)
        print(f"Server {self.pid} started on port {port}")
        self.delivery_thread = threading.Thread(target=self.deliver_events)
        self.delivery_thread.start()

    def update_clock(self, received_clock):
        self.clock = max(self.clock, received_clock) + 1

    def receive_message(self, sender_pid, received_clock, event):
        self.update_clock(received_clock)
        self.buffer.put((received_clock, (sender_pid, event)))
        print(f"Message received: {sender_pid}.{event}")

    def deliver_events(self):
        while True:
            if self.buffer.empty():
                time.sleep(0.1)
                continue

            _, (sender_pid, event) = self.buffer.get()
            print(f"Event delivered: {sender_pid}.{event}")

    def handle_client(self, client_socket):
        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            parts = data.split(":")
            sender_pid = int(parts[0])
            received_clock = int(parts[1])
            event = parts[2]
            self.receive_message(sender_pid, received_clock, event)
        client_socket.close()

    def start(self):
        while True:
            print("Server is waiting for connections...")
            client_socket, address = self.server_socket.accept()
            print(f"Connection accepted from {address}")
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

if __name__ == "__main__":
    pid = 0  # Set the process ID
    port = 5002  # Set the port number
    server = LamportMulticastServer(pid, port)
    server.start()
