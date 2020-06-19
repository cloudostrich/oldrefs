#!/usr/bin/env python3

import multiprocessing
from multiprocessing import Queue

q = Queue()

def mysum(i, numbers):
    total = 0
    for one_number in numbers:
        total += one_number
    q.put((i, total))

if __name__ == '__main__':
    processes = []
    for i in range(10):
        p = multiprocessing.Process(target=mysum, args=(i, range(i)))
        processes.append(p)
        p.start()

    for one_process in processes:
        p.join()

    while not q.empty():
        print(q.get())
