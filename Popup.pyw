#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from libs.appjar0900 import *
from libs.send import *
from libs.BlueFunc import *


def CloseIt():
	global AppMsg
	print("Msg Closed")
	AppMsg.stop()

AppMsg = gui("Message", "300x100", handleArgs=False)
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


AppMsg.setLocation(0, 0)
AppMsg.hideTitleBar()
AppMsg.setBg("#FFFFFF")
AppMsg.go()

