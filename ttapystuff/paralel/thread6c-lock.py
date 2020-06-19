import time
import random
import threading

lock = threading.Lock()

class BadQueue(object):
    def __init__(self):
        self.queue = [ ]
    def append(self, x):
        self.queue.append(x)
    def extend(self, x):
        print("Adding {}\n".format(x))
        with lock:
            for one_item in x:
                time.sleep(random.randint(1,2))
                self.queue.append(one_item)
    def __len__(self):
        return len(self.queue)
    def __repr__(self):
        return "BadQueue: {}".format(self.queue)

def add_to_queue(q, items):
    q.extend(items)

bq = BadQueue()
threads=[]

for i in range(5):
    t = threading.Thread(target=add_to_queue, args=(bq, range(10)))
    threads.append(t)
    t.start()

for one_thread in threads:
    one_thread.join()

print(bq)
