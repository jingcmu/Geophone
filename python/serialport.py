import serial

class SerialPort(object):

    def __init__(self, port, rate):
        """configure the serial connections"""
        super(SerialPort, self).__init__()
        self.ser = serial.Serial(
                port = port,
                baudrate = rate,
                parity = serial.PARITY_NONE,
                stopbits = serial.STOPBITS_ONE,
                bytesize = serial.EIGHTBITS,
                xonxoff = True
        )

    def readData(self):
        """
        read data from serial and return as an integer
        if -1, error is occurred, otherwise, return an integer
        """
        data = 0
        try:
            data = self.ser.readline()
        except ValueError:
            data = -1
        return data

