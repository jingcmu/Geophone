import Tkinter
import random

STEPNUM = 0

def detectedStep(a, b):
    randomNum = random.randint(a, b)
    if randomNum > 80:
        return True
    else:
        return False

def stepNum(a, b):
    global STEPNUM
    if detectedStep(a, b):
        STEPNUM = STEPNUM + 1
    return STEPNUM
     
def updateStepNumber(a, b):
    text.delete(1.0, 'end')
    text.insert('end', stepNum(a, b), 'BLUE')
    text.after(10, updateStepNumber, a, b)
    
def setText():
    text.tag_config('RED',foreground = 'red',font=('Tempus Sans ITC',400))
    text.tag_config('BLUE',foreground = 'blue',font=('Tempus Sans ITC',400))
 
if __name__ == '__main__':
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
    updateStepNumber(0, 100)
    window.mainloop()