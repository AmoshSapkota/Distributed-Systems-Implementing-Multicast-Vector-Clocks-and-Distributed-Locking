from kazoo.client import KazooClient
import threading
import time

class DistributedLockServer:
    def __init__(self, zk_hosts):
        self.zk = KazooClient(hosts=zk_hosts)
        self.zk.start()
        self.lock_path = "/distributed_lock"
        self.lock = self.zk.Lock(self.lock_path, "server")

    def acquire_lock(self):
        print("Trying to acquire lock...")
        self.lock.acquire()
        print("Lock acquired.")
        
        # Simulate some critical operation
        with open('shared_file.txt', 'r+') as f:
            counter = int(f.read().strip())
            counter += 1
            f.seek(0)
            f.write(str(counter))
            f.truncate()

        time.sleep(2)  # Simulate operation duration
        self.lock.release()
        print("Lock released.")

    def run(self):
        print("Server is running and waiting for clients...")
        while True:
            time.sleep(1)

if __name__ == "__main__":
    zk_hosts = '127.0.0.1:2181'
    server = DistributedLockServer(zk_hosts)
    server_thread = threading.Thread(target=server.run)
    server_thread.start()
