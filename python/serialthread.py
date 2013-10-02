import threading

import serialport
import time

class SerialThread(threading.Thread):
    def __init__(self, data, serial):
        super(SerialThread, self).__init__()
        self.data = data
        self.serial = serial
        self.isRunning = False
        self.lock = threading.Lock()

    def run(self):
        self.isRunning = True
        while self.isRunning:
            self.lockAcquire()
            data = self.serial.readData()
            if data == -1:
                continue
            # print data
            self.data.append(data)
            self.lockRelease()

    def stop(self):
        self.isRunning = False

    def lockAcquire(self):
        self.lock.acquire()

    def lockRelease(self):
        self.lock.release()

def openSerial(port, rate):
    """
    open serial with port and rate and return serial
    """
    return serialport.SerialPort(port, rate)

if __name__ == '__main__':
    # Serial port
    SERIAL_PORT = '/dev/ttyACM1'
    # Serial baudrate
    SERIAL_RATE = 115200
    dataList = []
    ser = openSerial(SERIAL_PORT, SERIAL_RATE)
    t = SerialThread(dataList, ser)
    t.start()
    time.sleep(1)
    t.lockAcquire()
    time.sleep(2)
    t.lockRelease()
    time.sleep(1)
    t.stop()

    for data in dataList:
        print data

