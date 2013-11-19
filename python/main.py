import Tkinter
import random

import serialport
import serialthread
import time
import copy

STEPNUM = 0

# Serial port
SERIAL_PORT = '/dev/tty.usbmodem11231'
# Serial baudrate
SERIAL_RATE = 115200

# Global list to store data from serial
dataList = []
data_processing = []
t = None

def detectedStep():
    global t
    global dataList
    global data_processing
    temp_data = []
    
    #t.lockAcquire()
    print 'len of datalist = ', len(dataList)
    
    if len(dataList) > 100:
        temp_data = copy.copy(dataList)
        dataList = []
        data_processing.extend(temp_data)
        #print data_processing
        #the window size for processing is 200
        #each time update 100 data
        if len(data_processing) > 200:
            data_processing = data_processing[100:]
        #t.lockRelease()
        if len(data_processing):
            max_data = max(data_processing)
        else:
            return False
        
        index_max = data_processing.index(max_data)
        #print 'index_max = ', index_max
        power = 0
    
        if len(data_processing) - index_max > 25 and index_max > 25:
            power = sum(data_processing[index_max-25:index_max+25])
            #print 'power = ', power
        else:
            return False
     
        if power > 500:
            return True
        else:
            return False
    else:
        return False
    return False
    
def stepNum():
    global STEPNUM
    global temp_data
    #t.lockAcquire()
    if detectedStep():
        STEPNUM = STEPNUM + 1
    return STEPNUM
    #t.lockRelease()
#      
# def updateStepNumber():
#     text.delete(1.0, 'end')
#     text.insert('end', stepNum(), 'BLUE')
#     text.after(10, updateStepNumber)
#     
# def setText():
#     text.tag_config('RED',foreground = 'red',font=('Tempus Sans ITC',400))
#     text.tag_config('BLUE',foreground = 'blue',font=('Tempus Sans ITC',400))
#  
def openSerial(port, rate):
    """
    open serial with port and rate and return serial
    """
    return serialport.SerialPort(port, rate)

def startThread(ser):
    """
    start a thread to read data from serial
    """
    global dataList
    global t
    t = serialthread.SerialThread(dataList, ser)
    if t:
        t.start()

if __name__ == '__main__':

    ser = openSerial(SERIAL_PORT, SERIAL_RATE)
    startThread(ser)
'''
    stepnum = 0
    #GUI main window
    window = Tkinter.Tk()
    #set window size
    window.geometry('1024x512')
    #init text widget
    text = Tkinter.Text(window)
    #pack text widget
    text.pack(expand=1, fill='both')
    setText()
    updateStepNumber()
    window.mainloop()

'''