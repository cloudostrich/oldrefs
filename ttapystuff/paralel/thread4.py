import threading

x = 12345
y = 'hello'
z = [10, 20, 30]

class MyClass(threading.Thread):

    def run(self):
        tid = threading.get_ident()
        print("Thread {0} has x = {1}, y = {2}, z = {3}".format(tid, x,y,z))

for i in range(5):
    t = MyClass()
    t.start()
