#!/usr/bin/env python3.6
#v4.2.2017
import os
import time
import tkinter
from tkinter import *

fileCODE=str
top1=tkinter.Tk()
top1.wm_title("Burkardt Barcode Suche")
entry1=Entry(top1)
entry2=Entry(top1)

# 
def add():
    if os.path.exists("AUTO"):
        AutoFile=open("AUTO-ADD", "w")
        AutoFile.write("1")
        AutoFile.close()
        autoA0()
    print("\nADD")
    CODE=entry1.get()
    print("CODE: " + CODE)
    CODELENGE=len(CODE)
    print("CODELENGE: " + str(CODELENGE))
    filename= str(CODELENGE) + "/" + CODE
    try:
        os.stat(str(CODELENGE))
    except:
        os.mkdir(str(CODELENGE))
    fileCODE=open(filename, "w") 
    SixCode=entry2.get()
    fileCODE.write(SixCode)
    print("Burkardt Code: " + SixCode)
    topAdd = Tk()
    topAdd.withdraw()
    topAdd.clipboard_clear()
    topAdd.clipboard_append(SixCode)
    topAdd.destroy()
    entry1.delete(0, END)
    entry2.delete(0, END)
    if os.path.exists("AUTO-ADD"):
        AutoFile=open("AUTO", "w")
        AutoFile.write("1")
        AutoFile.close()
        os.remove("AUTO-ADD")
        autoA1()

def revsuchen():
    print("\nREVSUCHEN")
    BCODE=entry1.get()
    print("Burkardt CODE: " + BCODE)
    #CODELENGE=1
    for CODELENGE in os.listdir("./"): 
        if CODELENGE.isdigit():
            if os.path.exists(CODELENGE + "/"): 
                for codedatei in os.listdir(CODELENGE): 
                    filename= str(CODELENGE) + "/" + codedatei
                    #try:
                    dateiinhalt=open(filename, "r").read()
                    if BCODE == dateiinhalt:
                        print("CODELENGE : " + CODELENGE + "	DATEI : " + codedatei + "	INHALT : " + dateiinhalt)
                    #except ValueError:
                     #   print(" ") 

def suchen():
    print("\nSUCHEN")
    CODE=entry1.get()
    print("CODE: " + CODE)
    CODELENGE=len(CODE)
    print("CODELENGE: " + str(CODELENGE))
    filename= str(CODELENGE) + "/" + CODE
    if os.path.exists(filename):
        fileCODE=open(filename, "r") 
        SixCode=fileCODE.read()
        print("Burkardt Code: " + SixCode)
        topAdd = Tk()
        topAdd.withdraw()
        #topAdd.clipboard_clear()
        topAdd.clipboard_append(SixCode)
        topAdd.destroy()
        entry1.delete(0, END)

def autofunc():
    if os.path.exists("AUTO"):
        print("AUTO FUNC")
        entry1.delete(0, END)
        topAdd = Tk()
        topAdd.withdraw()
        entry1.insert(END, topAdd.clipboard_get())
        topAdd.destroy() 
        suchen()

        top1.after(10, autofunc)

def autoA1():
    AutoFile=open("AUTO", "w")
    AutoFile.write("1")
    AutoFile.close()
    print("Auto ON")
    topAdd = Tk()
    topAdd.withdraw()
    topAdd.clipboard_append("0")
    topAdd.destroy() 
    autofunc()
  
def autoA0():
	os.remove("AUTO")
	print("Auto OFF")

def func(event):
    print("You hit return.")
    suchen()
top1.bind('<Return>', func)

button1=Button(top1, text="Suchen", command=suchen)
buttonA1=Button(top1, text="AUTO AN", command=autoA1)
buttonA0=Button(top1, text="AUTO AUS", command=autoA0)
button3=Button(top1, text="Hinzufugen", command=add)
button2=Button(top1, text="Orig. Suchen", command=revsuchen)

buttonA1.grid(row=3, column=0)
buttonA0.grid(row=3, column=1)
entry1.grid(row=0, column=0)
button1.grid(row=0, column=1)
button2.grid(row=0, column=2)
entry2.grid(row=2, column=0)
button3.grid(row=2, column=1) 



top1.mainloop()




