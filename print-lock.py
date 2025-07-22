import threading
import random
import time

print_lock = threading.Lock()

def download(filename):
    thread_name = threading.current_thread().name

    try:
        with print_lock:
            print(f"{thread_name} is starting download for {filename}")

        time.sleep(random.randint(10, 20) / 100)

        with print_lock:
            print(f"{thread_name} has completed download for {filename}")
    
    except:
        with print_lock:
            print(f"{thread_name} - Download interrupted for {filename}")

def main():
    files = ["file1.txt", "file2.txt", "file3.txt"]
    threads = []

    for i, f in enumerate(files):
        t = threading.Thread(target=download, args=(f,), name=f"Thread-{i+1}")
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

if __name__ == "__main__":
    main()