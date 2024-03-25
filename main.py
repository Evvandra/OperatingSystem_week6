import threading
import random

LOWER_NUM = 1
UPPER_NUM = 10000
BUFFER_SIZE = 100
MAX_COUNT = 10000

class BoundedBuffer:
    def __init__(self):
        self.buffer = []
        self.lock = threading.Lock()
        self.full = threading.Semaphore(0)
        self.empty = threading.Semaphore(BUFFER_SIZE)

    def push(self, item):
        self.empty.acquire()
        self.lock.acquire()
        self.buffer.append(item)
        self.lock.release()
        self.full.release()

    def pop(self):
        self.full.acquire()
        self.lock.acquire()
        item = self.buffer.pop()
        self.lock.release()
        self.empty.release()
        return item

def producer(buffer):
    for _ in range(MAX_COUNT):
        num = random.randint(LOWER_NUM, UPPER_NUM)
        with open('all.txt', 'a') as f:
            f.write(str(num) + '\n')
        buffer.push(num)

def customer(buffer, parity, filename):
    while True:
        num = buffer.pop()
        if num % 2 == parity:
            with open(filename, 'a') as f:
                f.write(str(num) + '\n')

if __name__ == "__main__":
    buffer = BoundedBuffer()
    producer_thread = threading.Thread(target=producer, args=(buffer,))
    customer_even_thread = threading.Thread(target=customer, args=(buffer, 0, 'even.txt'))
    customer_odd_thread = threading.Thread(target=customer, args=(buffer, 1, 'odd.txt'))

    producer_thread.start()
    customer_even_thread.start()
    customer_odd_thread.start()

    producer_thread.join()
    customer_even_thread.join()
    customer_odd_thread.join()



