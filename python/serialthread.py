#encoding:utf-8
import threading
import serialport
#import time
import FFT  # @UnresolvedImport

class SerialThread(threading.Thread):

    #缓存256ms数据
    SAMPLE_RATE = 10000   
    WINDOWSIZE = SAMPLE_RATE/5           #对200ms数据进行fft，得到fft能量
    BUFFSIZE = WINDOWSIZE * 2  
    SMOOTH_BUFFSIZE = 128
    VOLT = 337
    #VOLT = 512
     
    DT = 1 #单位是1/SAMPLE_RATE秒  
       
    #脚步探测
    stepNum = 0
    stepInterval = 0.3
    
    #power
    POWERTHRESHOLD = 0  
    POWERTHRESHOLD_TRAIN_INDEX = 0 
    TRAINING_TIME = 20     
    MULTIPLIOR = 1.4
    WINDOW_NUM = 20                 #存2秒的数据，目的：如果前一秒和后一秒都没有震动去掉孤立的震动
    
    def __init__(self, dataList, serial):
        super(SerialThread, self).__init__()
        self.smooth_datalist = []
        self.dataList = dataList
        self.serial = serial
        self.isRunning = False
        self.lock = threading.Lock()
        self.powerlist = []  #fft能量
        self.timeStamp = []  #相对buffer起始点的相对时间      
        self.stepRecord = [] #备选的脚步，0-不是脚步，1-是脚步
        
    def smooth(self, datalist, size):
        if size != 128:
            print "smooth buffer size need to change"
            return 0
        datasum = 0;
        for data in datalist:
            datasum = datasum + data     
        return datasum>>7
    
    #训练振动能量的阈值
    def powerTraining(self):
        power = FFT.getFFTPower(self.dataList)
        self.POWERTHRESHOLD = self.POWERTHRESHOLD + power
        print power #self.POWERTHRESHOLD 
        self.POWERTHRESHOLD_TRAIN_INDEX = self.POWERTHRESHOLD_TRAIN_INDEX + 1
        if self.POWERTHRESHOLD_TRAIN_INDEX == self.TRAINING_TIME:
            self.POWERTHRESHOLD = self.POWERTHRESHOLD/self.TRAINING_TIME
            print "powerThreshold:\n"
            print self.POWERTHRESHOLD
            self.POWERTHRESHOLD = self.POWERTHRESHOLD*self.MULTIPLIOR
            print "powerThreshold1:\n"
            print self.POWERTHRESHOLD
        #清空buffer前一半数据
        self.dataList = self.dataList[self.WINDOWSIZE:]
        
    #该线程的主函数
    def run(self):
        self.isRunning = True
        while self.isRunning:
            self.lockAcquire()
            print "before readData"
            data = self.serial.readData()
            print "after readData", data
            return
            #如果data太小（小于20）或者太大（大于1023），通常是读数据错误导致的
            if data < 20 or data > 1023:
                data = self.VOLT   #接3.3伏
                
            data = abs(data - self.VOLT)
            
            #填充smooth buffer
            self.smooth_datalist.append(data)
            if len(self.smooth_datalist) < self.SMOOTH_BUFFSIZE-1: #self.SMOOTH_BUFFSIZE-1 is 127
                continue
            
            data_smoothed = self.smooth(self.smooth_datalist, self.SMOOTH_BUFFSIZE)
            self.smooth_datalist = self.smooth_datalist[1:]
            self.dataList.append(data_smoothed)  #数据存入datalist
            
            #如果datalist的长度大于BUFFSIZE（256ms数据），则对前128ms的数据进行一次fft，并清空前128ms数据
            if len(self.dataList) > self.BUFFSIZE:
                
                if self.POWERTHRESHOLD_TRAIN_INDEX < self.TRAINING_TIME:
                    self.powerTraining()
                else:
                    #print "powerThreshold2:", self.POWERTHRESHOLD
                    self.detectStep()
            
            self.lockRelease()
    
    #如果peak span过小，去掉两个peak span中较小的一个
    #如果前一秒后一秒都没有脚步则去掉当前脚步
    def removeStep(self, step_record):
        size = len(step_record)
        if step_record[size/2] == 1 and sum(step_record) == 1:
            step_record[size/2] = 0
        
    
    #利用fft能量进行脚步检测
    #算法：
    #    0. 缓存3个128ms数据的fft能量，设为fft_a,fft_b,fft_c，如果满足下面条件，则判断为一个脚步
    # 条件1. fft_b-fft_a > threshold && fft_b-fft_c > threshold
    # 条件2. ...
    def detectStep(self):
        power = FFT.getFFTPower(self.dataList)
        tmp_buffer = self.dataList[:self.WINDOWSIZE/2]
        max_index = self.dataList.index(max(tmp_buffer))
        max_index = max_index + (self.WINDOW_NUM-1)*(self.WINDOWSIZE/2)
        print 'max_index', max_index
        
        self.timeStamp.append(max_index)
        self.powerlist.append(power)
        if len(self.powerlist) == self.WINDOW_NUM:
            #判断是否满足fft_b-fft_a > threshold && fft_b>fft_c > threshold
            if (self.powerlist[self.WINDOW_NUM-2] > self.powerlist[self.WINDOW_NUM-3]
                and self.powerlist[self.WINDOW_NUM-2] > self.powerlist[self.WINDOW_NUM-1]
                and self.powerlist[self.WINDOW_NUM-2] > self.POWERTHRESHOLD):
                
                self.stepRecord.append(1)
                #self.stepNum = self.stepNum + 1
                #print 'Step index :', self.stepNum
                #print 'Power = ', self.powerlist[1]
            else:
                self.stepRecord.append(0)
            
            #清掉第一个power, 只维持WINDOW_NUM个
            self.powerlist = self.powerlist[1:]
            
            #填充stepRecord
            if len(self.stepRecord) < self.WINDOW_NUM:
                return
                
            #如果peak span过小，去掉两个peak span中较小的一个
            #如果前一秒后一秒都没有脚步则去掉当前脚步
            self.removeStep(self.step_record)
           
            for i in xrange(len(self.timeStamp)-1):
                self.timeStamp[i] = self.timeStamp[i] - (self.WINDOWSIZE/2)
            
            print '[', self.timeStamp, ']'   
              
            #print self.powerlist
            
            #清掉第一个timeStamp,只维持WINDOW_NUM个
            self.timeStamp = self.timeStamp[1:]
            #清掉第一个stepRecord, 只维持WINDOW_NUM个
            self.stepRecord = self.stepRecord[1:]
              
        else:
            self.stepRecord.append(0)
        
        size = len(self.stepRecord)
        if self.stepRecord[size/2] == 1:
            self.stepNum = self.stepNum + 1
            print 'Step index :', self.stepNum
            print 'Power = ', self.powerlist[size/2]
            
        #清空buffer前一半数据
        self.dataList = self.dataList[self.WINDOWSIZE/2:]

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
