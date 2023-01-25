import time
import keyboard
from tkinter import *
from tkinter.ttk import *

class LabelInit:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.time = 0
        self.stopped = False
        self.label = None

    def initLabel(self, label):
        self.label = label

    def stopTime(self):
        self.time = time.time() - start_zeit
        self.stopped = True

start_zeit = 0
labelcontainer: dict[str, LabelInit] = {}
started = False

labelInit = {
    "1" : LabelInit(200, 12),
    "2" : LabelInit(200, 42),
    "3" : LabelInit(200, 72),
    "4" : LabelInit(200, 102),
    "5" : LabelInit(200, 132),
    "6" : LabelInit(200, 162),
}

def start():
    global start_zeit, started
    start_zeit = time.time()

    if len(labelcontainer) == 0:
        for i in labelInit:
            label = Label(root, text="0:00")
            labelcontainer[i] = labelInit.get(i)
            labelcontainer[i].initLabel(label)
            label.place(x=labelInit.get(i).x, y=labelInit.get(i).y)
    else:
        for counter in labelcontainer:
            labelcontainer.get(counter).stopped = False

    started = True

    updateLoop()

def updateLoop():
    while started:
        for counter in labelcontainer:
            # stops program completely
            time.sleep(0.01)
            if not labelcontainer.get(counter).stopped:
                labelcontainer.get(counter).label.config(text="{0:.3f}".format(time.time() - start_zeit))

        root.update()

def stopAll():
    global labelcontainer

    for counter in labelcontainer:
        curlabel = labelcontainer.get(counter)
        curlabel.label.config(text="0:00")
        curlabel.stopTime()

    started = False

def startbutton():
    start()
    label = Label(root, text=("Die Stopuhr wurde Gestartet"))
    label.place(x=80, y=190)

def resetbutton():
    stopAll()
    label = Label(root, text=("Die Stopuhr wurde Gestoppt"))
    label.place(x=80, y=190)

def stop (h, v, buttonID):
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
root.geometry("300x220")
root.configure(bg="#86354A")

start_button = Button(root, text="Start", command=startbutton).place(x=15, y=10)

stop_button1 = Button(root, text="Stop", command=lambda: stop(200, 12, 1)).place(x=115, y=10)
stop_button2 = Button(root, text="Stop", command=lambda: stop(200, 42, 2)).place(x=115, y=40)
stop_button3 = Button(root, text="Stop", command=lambda: stop(200, 72, 3)).place(x=115, y=70)
stop_button4 = Button(root, text="Stop", command=lambda: stop(200, 102, 4)).place(x=115, y=100)
stop_button5 = Button(root, text="Stop", command=lambda: stop(200, 132, 5)).place(x=115, y=130)
stop_button6 = Button(root, text="Stop", command=lambda: stop(200, 162, 6)).place(x=115, y=160)

reset_button = Button(root, text="Reset", command=resetbutton).place(x=15, y=40)

root.mainloop()