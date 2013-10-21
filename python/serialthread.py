#encoding:utf-8
import threading
import serialport
import time
import FFT

class SerialThread(threading.Thread):
    stepNum = 0
    #缓存256ms数据
    BUFFSIZE = 256                
    WINDOWSIZE = BUFFSIZE/2       #对128ms数据进行fft，得到fft能量
    
    #power
    POWERTHRESHOLD = 16000        
    
    def __init__(self, dataList, serial):
        super(SerialThread, self).__init__()
        self.dataList = dataList
        self.serial = serial
        self.isRunning = False
        self.lock = threading.Lock()
        self.powerlist = []
    
    #该线程的主函数
    def run(self):
        self.isRunning = True
        while self.isRunning:
            self.lockAcquire()
            data = self.serial.readData()
            #如果data太小（小于20）或者太大（大于1023），通常是读数据错误导致的
            if data < 20 or data > 1023:
                data = 512
            data = abs(data - 512)
            #print data,
            self.dataList.append(data)  #数据存入datalist
            #如果datalist的长度大于BUFFSIZE（256ms数据），则对前128ms的数据进行一次fft，并清空前128ms数据
            if len(self.dataList) > self.BUFFSIZE:
                self.detectStep()
            self.lockRelease()
    
    #利用fft能量进行脚步检测
    #算法：
    #    0. 缓存3个128ms数据的fft能量，设为fft_a,fft_b,fft_c，如果满足下面条件，则判断为一个脚步
    # 条件1. fft_b-fft_a > threshold && fft_b>fft_c > threshold
    # 条件2. ...
    def detectStep(self):
        power = FFT.getFFTPower(self.dataList)
        self.powerlist.append(power)
        if len(self.powerlist) == 3:
            #判断是否满足fft_b-fft_a > threshold && fft_b>fft_c > threshold
            if (self.powerlist[1] - self.powerlist[0]>self.POWERTHRESHOLD\
                and self.powerlist[1] - self.powerlist[2]>self.POWERTHRESHOLD):
                self.stepNum = self.stepNum + 1
                print 'Step ', self.stepNum
            #清掉第一个power
            print self.powerlist
            self.powerlist = self.powerlist[1:]
        
        #清空前128ms数据
        self.dataList = self.dataList[self.WINDOWSIZE:]

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
