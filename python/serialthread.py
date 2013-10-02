import threading

import serialport
import time


class SerialThread(threading.Thread):
    stepNum = 0
    BUFFSIZE = 400
    WINDOWSIZE = BUFFSIZE/2
    HALFWINOW = WINDOWSIZE/2
    DENSITY = 6
    THRESHDATA = 10
    NUM = 20
    
    #power
    POWERTHRESHOLD = 16000        #strength is normally less than 5
    #sum
    #POWERTHRESHOLD = 4*200        #strength is normally less than 5

    
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
            if data < 20 or data > 1023:
                data = 512
            data = abs(data - 512)
            #print data,
            #use power to decide:
            if data < self.THRESHDATA:
                data = 0
            #self.data.append(data*data)
            self.data.append(data*data)
            
            #windon size is 200
            if len(self.data) > self.BUFFSIZE:
                self.detectStep()
            self.lockRelease()
    
    def detectStep(self):
        max_data = max(self.data)
        index_max = self.data.index(max_data)
        power = 0
        density = 0
        
        if len(self.data) - index_max > self.HALFWINOW and index_max > self.HALFWINOW:
            power = sum(self.data[index_max - self.HALFWINOW : index_max + self.HALFWINOW])
            
            for d in self.data:
                if d > self.THRESHDATA:
                    density = density + 1
            
            #if density > self.NUM:
            if power > self.POWERTHRESHOLD:
                self.stepNum = self.stepNum + 1
                print 'Step ', self.stepNum
                print 'Power = ', power
                print self.data[index_max - self.HALFWINOW : index_max + self.HALFWINOW]
  
            self.data[index_max-self.HALFWINOW:index_max+self.HALFWINOW] = [0]*self.WINDOWSIZE

        #clear first half data
        self.data = self.data[self.WINDOWSIZE:]
        
        

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

