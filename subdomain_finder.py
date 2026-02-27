import socket
import threading
from queue import Queue

domain = input("Enter target domain (example.com): ")
wordlist_file = input("Enter wordlist file path: ")

queue = Queue()

try:
    with open(wordlist_file, "r") as f:
        for line in f:
            queue.put(line.strip())
except FileNotFoundError:
    print("Wordlist not found!")
    exit()

def scan_subdomain():
    while not queue.empty():
        sub = queue.get()
        full_domain = f"{sub}.{domain}"
        try:
            ip = socket.gethostbyname(full_domain)
            print(f"[+] Found: {full_domain} --> {ip}")
        except:
            pass
        queue.task_done()

thread_count = 50

for _ in range(thread_count):
    t = threading.Thread(target=scan_subdomain)
    t.start()

queue.join()

print("Subdomain scanning completed.")
