#!/usr/bin/env python3

import threading
import time
import random
from queue import Queue   # in Python 2, the module is "Queue"

q = Queue()

def putter():
    for i in range(10):
        print("[Putter] Putting {}".format(i))
        q.put(i)

        time_to_sleep = random.randint(1,2)
        print("[Putter] Sleeping {} seconds".format(time_to_sleep))

        time.sleep(time_to_sleep)
    print("[Putter] We're done; sending None")
    q.put(None)
    
def getter():
    while True:
        print("\t[Getter] Getting from queue")
        number = q.get()
        if number is None:
                print("\t[Getter] Got None; I'm done!")
                break

        print("\t[Getter] Got {} from queue".format(number))

        time_to_sleep = random.randint(4,8)
        print("\t[Getter] Sleeping {} seconds".format(time_to_sleep))
        time.sleep(time_to_sleep)

print("Starting both threads")
t1 = threading.Thread(target=putter)
t1.start()

t2 = threading.Thread(target=getter)
t2.start()

t1.join()
t2.join()

print("Both threads ended")
