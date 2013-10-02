import threading

# import serialport

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
            # print data
            self.data.append(data)
            self.lockRelease()

    def stop(self):
        self.isRunning = False

    def lockAcquire(self):
        self.lock.acquire()

    def lockRelease(self):
        self.lock.release()

# def openSerial(port, rate):
#     """
#     open serial with port and rate and return serial
#     """
#     return serialport.SerialPort(port, rate)

# if __name__ == '__main__':
#     # Serial port
#     SERIAL_PORT = '/dev/ttyACM0'
#     # Serial baudrate
#     SERIAL_RATE = 115200
#     ser = openSerial(SERIAL_PORT, SERIAL_RATE)
#     t = SerialThread([], ser)
#     t.start()

