import time
import os
from tkinter import *
from tkinter.ttk import *
import RPi.GPIO as GPIO

# used for dev
if os.environ.get('DISPLAY', '') == '':
    print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')


class LabelInit:
    def __init__(self, x, y, pin):
        self.x = x
        self.y = y
        self.pin = pin
        self.time = 0
        self.stopped = False
        self.label = None

    def initPin(self):
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def initLabel(self, label):
        self.label = label

    def stopTime(self):
        print(f"Button {self.pin} wurde gestoppt!")
        self.time = time.time() - start_zeit
        self.stopped = True


start_zeit = 0
labelcontainer: dict[str, LabelInit] = {}
started = False

labelInit = {
    "1": LabelInit(285, 80, 17),
    "2": LabelInit(285, 260, 27),
    "3": LabelInit(285, 440, 22),
    "4": LabelInit(720, 80, 5),
    "5": LabelInit(720, 260, 6),
    "6": LabelInit(720, 440, 26)
}

gpiolist = [23, 24]


def initGPIO():
    GPIO.setmode(GPIO.BCM)

    for gpio in gpiolist:
        GPIO.setup(gpio, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


initGPIO()


def start():
    global start_zeit, started
    start_zeit = time.time()

    if len(labelcontainer) == 0:
        for i in labelInit:
            curlabel = labelInit.get(i)

            label = Label(root, text="0:00")
            labelcontainer[i] = curlabel
            labelcontainer[i].initLabel(label)
            label.place(x=curlabel.x, y=curlabel.y)
            curlabel.initPin()
    else:
        for counter in labelcontainer:
            labelcontainer.get(counter).stopped = False

    started = True

    updateLoop()


def updateLoop():
    while started:
        for counter in labelcontainer:
            curlable: LabelInit = labelcontainer.get(counter)

            if GPIO.input(curlable.pin) and not curlable.stopped:
                stop(counter)

            if not curlable.stopped:
                curlable.label.config(
                    text="{0:.3f}".format(time.time() - start_zeit))

        if GPIO.input(gpiolist[1]):
            stopAll()

        root.update()


def stopAll():
    global labelcontainer, started

    for counter in labelcontainer:
        curlabel = labelcontainer.get(counter)
        curlabel.label.config(text="0:00")
        curlabel.stopTime()

    started = False


def stop(buttonID: str):
    global start_zeit
    global labelcontainer

    endzeit_bahn_einz = time.time()
    zeit_bahn_einz = endzeit_bahn_einz - start_zeit
    i = round(zeit_bahn_einz, 2)

    if labelcontainer.get(f"{buttonID}").stopped:
        print("YEET")
    else:
        labelcontainer.get(f"{buttonID}").stopTime()


root = Tk()
root.title("stopuhr")
root.geometry("1000x1000")
root.configure(bg="#86354A")


def initStopButton(y_start):
    Button(root, text="Bahn 1", command=lambda: stop(1)).place(x=35, y=y_start+30, height=100, width=200)
    Button(root, text="Bahn 2", command=lambda: stop(2)).place(x=35, y=y_start+30*7, height=100, width=200)
    Button(root, text="Bahn 3", command=lambda: stop(3)).place(x=35, y=y_start+30*13, height=100, width=200)
    Button(root, text="Bahn 4", command=lambda: stop(4)).place(x=470, y=y_start+30, height=100, width=200)
    Button(root, text="Bahn 5", command=lambda: stop(5)).place(x=470, y=y_start+30*7, height=100, width=200)
    Button(root, text="Bahn 6", command=lambda: stop(6)).place(x=470, y=y_start+30*13, height=100, width=200)
    


start_button = Button(root, text="Start",
                      command=start).place(x=850, y=50, height=75, width=125)

initStopButton(10)

def isStartButtonPressed():
    if GPIO.input(gpiolist[0]) and not started:
        start()

    root.after(10, isStartButtonPressed)
        


reset_button = Button(root, text="Reset",
                      command=stopAll).place(x=850, y=410, height=75, width=125)
root.after(10, isStartButtonPressed)
root.mainloop()
GPIO.cleanup()
