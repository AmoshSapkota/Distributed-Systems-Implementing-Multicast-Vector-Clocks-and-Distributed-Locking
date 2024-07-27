from kazoo.client import KazooClient
import threading
import time

class DistributedLockClient:
    def __init__(self, pid, zk_hosts):
        self.pid = pid
        self.zk = KazooClient(hosts=zk_hosts)
        self.zk.start()
        self.lock_path = "/distributed_lock"
        self.lock = self.zk.Lock(self.lock_path, f"client-{pid}")

    def acquire_lock(self):
        print(f"Client {self.pid} is trying to acquire the lock...")
        self.lock.acquire()
        print(f"Client {self.pid} has acquired the lock.")

        # Simulate some critical operation
        with open('shared_file.txt', 'r+') as f:
            counter = int(f.read().strip())
            counter += 1
            f.seek(0)
            f.write(str(counter))
            f.truncate()

        time.sleep(2)  # Simulate operation duration
        self.lock.release()
        print(f"Client {self.pid} has released the lock.")

    def run(self):
        for _ in range(3):  # Acquire lock 3 times
            self.acquire_lock()
            time.sleep(1)

if __name__ == "__main__":
    zk_hosts = '127.0.0.1:2181'
    num_clients = 3

    threads = []
    for pid in range(num_clients):
        client = DistributedLockClient(pid, zk_hosts)
        t = threading.Thread(target=client.run)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()
