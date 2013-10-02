import threading

class SerialThread(threading.Thread):
    def __init__(self, data, serial):
        super(SerialThread, self).__init__()
        self.data = data
        self.serial = serial
        self.isRunning = False
        self.cv = threading.Condition()

    def run(self):
        self.isRunning = True
        self.cv.acquire()
        while self.isRunning:
            # Do something useful
            self.cv.wait()

    def stop(self):
        self.isRunning = False

    def lock(self):
        self.lock.acquire()

    def release(self):
        self.lock.release()

if __name__ == '__main__':
    SerialThread(1, 2).start()
