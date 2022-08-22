import matplotlib.pyplot as plt
import os
import tkinter

#initializers
headers = []
times = []

def GUI():
    m = tkinter.Tk()
    m.title("Karting Grapher")
    m.geometry("1000x200")
    label_file_explorer = tkinter.Label(m,text="Welcome to the kart timing plotter. To use browse the file with times. \nIt is important that the times do not have letters or symbols on the same line and that the timings are seperated by a header(e.g. session1). \nEmpty lines are allowed to be in the txt file",width = 120, height = 3, fg="blue")
    button_explore = tkinter.Button(m,text = "Browse data", command= getData)
    button_exit = tkinter.Button(m,text= "Exit", command= exit)

    label_file_explorer.grid(column=1,row=1)
    button_explore.grid(column=1,row=2)
    button_exit.grid(column=1,row=3)
    m.mainloop()
    return
def startApplication():
    GUI()
    return

def getData():
    data = openFile()
    index = -1
    for line in data:
        line = line.strip()
        if line != "":
            if isHeader(line):
                headers.append(line)
                times.append([])
                index +=1
            else:
                times[index].append(float(line))
    plotData(20)
    return
def plotData(amountOfYTicks):
    for i in range(0,len(times)):
        laps = range(0,len(times[i]))
        plt.plot(laps,times[i], marker='o', label=headers[i])
        plt.legend()
        plt.xlabel("lap")
        plt.ylabel("lap time")
        plt.xticks(laps)
        plt.yticks(getYTicks(times[i],amountOfYTicks))
        plt.grid(True)
    plt.show()
    plt.close()

def openFile():
    while True:
        try:
            from tkinter import filedialog
            filename = tkinter.filedialog.askopenfilename(initialdir = "/", title = "Select a File", filetypes= (("Text files", "*.txt*"), ("all files","*.*" )))
            print(filename)
            file = open(filename, 'r', encoding='utf-8-sig')
            return file
        except(Exception):
            print("File not found try again\n(include the extension and the file should be in the same directory as this .py file)")

def isHeader(strToCheck):
    for char in strToCheck:
        if str(char).isalpha():
            return True
    return False
def getYTicks(t :list,amountOfYTicks:int):
    amountOfYTicks -= 2
    inBetween = []
    maxT = max(t)
    minT = min(t)
    diff = maxT - minT
    diffOnScale = diff/amountOfYTicks
    for x in range(-1,amountOfYTicks+1):
        inBetween.append(minT + x*diffOnScale)
    return inBetween





###main

startApplication()