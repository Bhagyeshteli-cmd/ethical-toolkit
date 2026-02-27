import socket
import threading
from queue import Queue

target = input("Enter target IP or domain: ")
start_port = int(input("Start port: "))
end_port = int(input("End port: "))

queue = Queue()

def scan_port(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, port))
        if result == 0:
            print(f"[+] Port {port} is OPEN")
        sock.close()
    except:
        pass

def worker():
    while not queue.empty():
        port = queue.get()
        scan_port(port)
        queue.task_done()

for port in range(start_port, end_port + 1):
    queue.put(port)

thread_count = 100

for _ in range(thread_count):
    t = threading.Thread(target=worker)
    t.start()

queue.join()

print("Scanning completed.")
