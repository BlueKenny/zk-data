#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from libs.appjar0830 import *
from libs.send import *
from libs.BlueFunc import *


def CloseIt():
	global AppMsg
	global MyPos
	print("Msg Closed")
	BlueSave(str(MyPos), "None", "DATA/POPUP")
	AppMsg.stop()

def NewPos():
	print("NewPos")
	global AppMsg
	global MyPos

	if MyPos == 2:
		if str(BlueLoad(str(MyPos-1), "DATA/POPUP")) == "None":
			BlueSave(str(MyPos-1), "False", "DATA/POPUP")
			BlueSave(str(MyPos), "None", "DATA/POPUP")
			MyPos = MyPos - 1
			AppMsg.setLocation(0, 0)

	if MyPos == 3:
		if str(BlueLoad(str(MyPos-1), "DATA/POPUP")) == "None":
			BlueSave(str(MyPos-1), "False", "DATA/POPUP")
			BlueSave(str(MyPos), "None", "DATA/POPUP")
			MyPos = MyPos - 1
			AppMsg.setLocation(0, 100)

AppMsg = gui("Message", "300x100", handleArgs=False)
#AppMsg.attributes("-topmost", True)
AppMsg.topLevel.attributes("-topmost", True)

print("sys.argv: " + str(sys.argv))

ID = sys.argv[1]
if ID == "0": # Nothing found
	AppMsg.addLabel("ArtInfo", sys.argv[2] + "\nis nicht im Stock")
	AppMsg.after(5000, CloseIt)
if ID == "PowerOff":
	AppMsg.addLabel("Info", "ACHTUNG\ndieser PC geht in " + sys.argv[2] + " sekunden aus")
	AppMsg.after(10000, CloseIt)
if not ID == "0" and not ID == "PowerOff":
	DATA_INFO = StockGetArtInfo(["Name", "Anzahl", "Ort"], ID).split(" | ")
	print(DATA_INFO)
	AppMsg.addLabel("ArtInfo", DATA_INFO[2] + "x " + DATA_INFO[1] + "\nOrt: " + DATA_INFO[3])
	AppMsg.after(20000, CloseIt)

Pop1Free = False
Pop2Free = False
Pop3Free = False
Pop1 = str(BlueLoad("1", "DATA/POPUP"))
Pop2 = str(BlueLoad("2", "DATA/POPUP"))
Pop3 = str(BlueLoad("3", "DATA/POPUP"))
if Pop1 == "None": Pop1Free = True
if Pop2 == "None": Pop2Free = True
if Pop3 == "None": Pop3Free = True

if Pop1Free:
	BlueSave("1", "False", "DATA/POPUP")
	MyPos = 1
	AppMsg.setLocation(0, 0)
else:
	if Pop2Free:
		BlueSave("2", "False", "DATA/POPUP")
		MyPos = 2
		AppMsg.setLocation(0, 100)
	else:
		BlueSave("3", "False", "DATA/POPUP")
		MyPos = 3
		AppMsg.setLocation(0, 200)

AppMsg.after(100, NewPos)


AppMsg.hideTitleBar()
AppMsg.setBg("#FFFFFF")
AppMsg.go()

