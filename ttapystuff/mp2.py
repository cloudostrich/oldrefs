#!/usr/bin/env python3

import multiprocessing
import time
import random

def write_abc(filename, i):
    print("Writing to {} with i = {}".format(filename, i))
    with open(filename, 'a') as f:
        for word in 'abc def ghi jkl mno'.split():
            time.sleep(random.randint(1,3))
            f.write("{}: {}\n".format(i, word))
            f.flush()

if __name__ == '__main__':
    for i in range(5):
        multiprocessing.Process(target=write_abc, args=('stuff.txt', i)).start()
