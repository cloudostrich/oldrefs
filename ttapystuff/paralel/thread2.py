import threading
import random
import time

class Myclass(threading.Thread):
    def run(self):
        s = random.randint(1,5)
        print('sleeping for {}'.format(s))
        time.sleep(s)
        print('wake up liao')
        
for i in range(5):
    Myclass().start()
