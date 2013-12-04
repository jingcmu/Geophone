#encoding:utf-8
import threading
import serialport
#import time
import FFT  # @UnresolvedImport

class SerialThread(threading.Thread):
    stepNum0 = 0
    stepNum1 = 0
    
    WINDOWSIZE = 200           #对200ms数据进行fft，得到fft能量
    #缓存256ms数据
    BUFFSIZE = WINDOWSIZE * 2                

    #power
    POWERTHRESHOLD0 = 0  
    POWERTHRESHOLD1 = 0 
    POWERTHRESHOLD_TRAIN_INDEX0 = 0 
    POWERTHRESHOLD_TRAIN_INDEX1 = 0 
    TRAINING_TIME0 = 50   
    TRAINING_TIME1 = 50    
    MULTIPLIOR = 1.4
    
    def __init__(self, dataList, serial):
        super(SerialThread, self).__init__()
        self.dataList0 = []
        self.dataList1 = []
        self.serial = serial
        self.isRunning = False
        self.lock = threading.Lock()
        self.powerlist0 = []
        self.powerlist1 = []
    
    #训练振动能量的阈值
    def powerTraining0(self):
        power = FFT.getFFTPower(self.dataList0)
        self.POWERTHRESHOLD0 = self.POWERTHRESHOLD0 + power
        print "power0 = ", power #self.POWERTHRESHOLD 
        self.POWERTHRESHOLD_TRAIN_INDEX0 = self.POWERTHRESHOLD_TRAIN_INDEX0 + 1
        if self.POWERTHRESHOLD_TRAIN_INDEX0 == self.TRAINING_TIME0:
            self.POWERTHRESHOLD0 = self.POWERTHRESHOLD0/self.TRAINING_TIME0
            print "powerThreshold0:\n"
            print self.POWERTHRESHOLD0
            self.POWERTHRESHOLD0 = self.POWERTHRESHOLD0*self.MULTIPLIOR
            print "powerThreshold0:\n"
            print self.POWERTHRESHOLD0
        #清空前128ms数据
        self.dataList0 = self.dataList0[self.WINDOWSIZE/2:]
     
    #训练振动能量的阈值
    def powerTraining1(self):
        power = FFT.getFFTPower(self.dataList1)
        self.POWERTHRESHOLD1 = self.POWERTHRESHOLD1 + power
        print "power1 = ", power #self.POWERTHRESHOLD 
        self.POWERTHRESHOLD_TRAIN_INDEX1 = self.POWERTHRESHOLD_TRAIN_INDEX1 + 1
        if self.POWERTHRESHOLD_TRAIN_INDEX1 == self.TRAINING_TIME1:
            self.POWERTHRESHOLD1 = self.POWERTHRESHOLD1/self.TRAINING_TIME1
            print "powerThreshold1:\n"
            print self.POWERTHRESHOLD1
            self.POWERTHRESHOLD1 = self.POWERTHRESHOLD1*self.MULTIPLIOR
            print "powerThreshold1:\n"
            print self.POWERTHRESHOLD1
        #清空前128ms数据
        self.dataList1 = self.dataList1[self.WINDOWSIZE/2:]
        
        
    #该线程的主函数
    def run(self):
        self.isRunning = True
        while self.isRunning:
            self.lockAcquire()
            data = self.serial.readData()
            data_int = data.split(',')
            try:
                data0 = int(data_int[0])
                data1 = int(data_int[1])
            except:
                data0 = 512
                data1 = 512
            #如果data太小（小于20）或者太大（大于1023），通常是读数据错误导致的
            if data0 < 20 or data0 > 1023:
                data0 = 512
                
            if data1 < 20 or data1 > 1023:
                data1 = 512
                
            data0 = abs(data0 - 512)
            data1 = abs(data1 - 512)
            #print data0, data1
            
            self.dataList0.append(data0)  #数据存入datalist
            self.dataList1.append(data1)  #数据存入datalist
            
            #如果datalist的长度大于BUFFSIZE（256ms数据），则对前128ms的数据进行一次fft，并清空前128ms数据
            if len(self.dataList0) > self.BUFFSIZE:
                if self.POWERTHRESHOLD_TRAIN_INDEX0 < self.TRAINING_TIME0:
                    self.powerTraining0()
                else:
                    #print "powerThreshold2:", self.POWERTHRESHOLD
                    self.detectStep0()
            
            if len(self.dataList1) > self.BUFFSIZE:
                if self.POWERTHRESHOLD_TRAIN_INDEX1 < self.TRAINING_TIME1:
                    self.powerTraining1()
                else:
                    #print "powerThreshold2:", self.POWERTHRESHOLD
                    self.detectStep1()
            
            self.lockRelease()
    
    #利用fft能量进行脚步检测
    #算法：
    #    0. 缓存3个128ms数据的fft能量，设为fft_a,fft_b,fft_c，如果满足下面条件，则判断为一个脚步
    # 条件1. fft_b-fft_a > threshold && fft_b-fft_c > threshold
    # 条件2. ...
    def detectStep0(self):
        power = FFT.getFFTPower(self.dataList0)
        self.powerlist0.append(power)
        if len(self.powerlist0) == 3:
            #判断是否满足fft_b-fft_a > threshold && fft_b>fft_c > threshold
            if (self.powerlist0[1] > self.powerlist0[0]
                and self.powerlist0[1] > self.powerlist0[2]
                and self.powerlist0[1] > self.POWERTHRESHOLD0):
                self.stepNum0 = self.stepNum0 + 1
                print 'GEO 0 Step index :', self.stepNum0
                print 'GEO 0 Power = ', self.powerlist0[1] 
            #清掉第一个power
            #print self.powerlist0
            self.powerlist0 = self.powerlist0[1:]
        #清空前100ms数据
        self.dataList0 = self.dataList0[self.WINDOWSIZE/2:]
        
    def detectStep1(self):
        power = FFT.getFFTPower(self.dataList1)
        self.powerlist1.append(power)
        if len(self.powerlist1) == 3:
            #判断是否满足fft_b-fft_a > threshold && fft_b>fft_c > threshold
            if (self.powerlist1[1] > self.powerlist1[0]
                and self.powerlist1[1] > self.powerlist1[2]
                and self.powerlist1[1] > self.POWERTHRESHOLD1):
                self.stepNum1 = self.stepNum1 + 1
                print 'GEO 1 Step index :', self.stepNum1
                print 'GEO 1 Power = ', self.powerlist1[1] 
            #清掉第一个power
            #print self.powerlist1
            self.powerlist1 = self.powerlist1[1:]  
        #清空前100ms数据
        self.dataList1 = self.dataList1[self.WINDOWSIZE/2:]

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
