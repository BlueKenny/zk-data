#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

from libs.appjar0900 import gui
from libs.RoundUp import *
from libs.debug import Debug
from libs.BlueFunc import *
from libs.send import *
from libs.barcode import *
import platform
import sys


EntryList=["Barcode", "Artikel", "Artikel2", "Artikel3", "Lieferant", "Name", "Ort", "PreisEK", "PreisVKH", "PreisVK"]

if len(sys.argv) == 1:
	ID = StockSetBCode()
	IDExists = False
else:
	ID = sys.argv[1]
	IDExists = True

def Save():
    global Time
    print("Save")
    print("Time " + str(Time))
    if not GetArt(ID)["LastChange"] == DATA_LOCAL["LastChange"]:
        appChange.infoBox("Achtung", "Dieser Artikel wurde gerade von einem anderen ort aus geändert", parent=None)
    else:
        print("Send Data to Server")
        SetArt(ID)
    return True

def VerifyInput(Entry):
	print("VerifyInput")
	Float = ["PreisEK", "PreisVKH", "PreisVK"]
	Int = ["Barcode"]
	String = ["Artikel", "Artikel2", "Artikel3", "Lieferant", "Name", "Ort"]
	print("Verify Entry " + str(Entry))
	appChange.setEntry(Entry, appChange.getEntry(Entry).replace("?", ""))

	if Entry == "Ort":
		print("Verify this input " + str(appChange.getEntry(Entry)))
		myLocation = appChange.getEntry(Entry).replace(",", ".").upper()
		appChange.setEntry(Entry, myLocation)

	if Entry in Int:
		print("Verify this input " + str(appChange.getEntry(Entry)))
		myInt = appChange.getEntry(Entry)
		appChange.setEntryMaxLength(Entry, 13)
		try:	
			appChange.setEntry(Entry, int(myInt))
			if Entry == "Barcode":
				if not len(appChange.getEntry(Entry)) == 13:
					appChange.setEntry(Entry, IDToBarcode(ID))
					appChange.infoBox("Achtung", "Dieser Barcode ist ungültig und wird jetzt neu generiert")
		except:
			if Entry == "Barcode":	appChange.setEntry(Entry, IDToBarcode(ID))
			else: appChange.setEntry(Entry, "0")
	if Entry in Float:
		print("Verify this input " + str(appChange.getEntry(Entry)))
		myFloat = appChange.getEntry(Entry)
		myFloat = myFloat.replace(",", ".")
		myFloat = myFloat.replace("..", ".")
		myFloat = myFloat.replace(".0.", ".")
		try:
			if Entry == "PreisEK":
				print("PreisEK")
				myFloat = RoundUp0000(myFloat)
				appChange.setEntry(Entry, float(myFloat))
			if Entry == "PreisVKH":
				print("PreisVKH")
				myFloat = RoundUp0000(myFloat)
				appChange.setEntry("PreisVK", RoundUp05(myFloat*1.21), callFunction=False)
				myFloat = RoundUp0000(float(appChange.getEntry("PreisVK"))/1.21)
				appChange.setEntry(Entry, float(myFloat))
			if Entry == "PreisVK":
				print("PreisVK")
				myFloat = RoundUp05(myFloat)
				appChange.setEntry("PreisVKH", RoundUp0000(myFloat/1.2100), callFunction=False)
				myFloat = RoundUp05(float(appChange.getEntry("PreisVKH"))*1.21)
				appChange.setEntry(Entry, float(myFloat))
		except:
			appChange.setEntry(Entry, "")
	DATA_LOCAL[Entry] = appChange.getEntry(Entry)
			
			
	

def VerifyChanges():
	print("VerifyChanges")
	if not DATA == DATA_LOCAL: UserMadeChanges= True
    else: UserMadeChanges = False
	if UserMadeChanges:
		if appChange.yesNoBox("Speichern", "Wollen sie speichern?", parent=None):
			if Save():
				BlueSave("LastID", ID, "DATA/DATA")
				return True
			else:
				BlueSave("LastID", ID, "DATA/DATA")
				appChange.infoBox("Speichern", "änderungen wurden nicht gespeichert", parent=None)
				return False
		else:
			BlueSave("LastID", ID, "DATA/DATA")
			return True
	else:
		BlueSave("LastID", ID, "DATA/DATA")
		return True

def BtnStockGraph(btn):
	if platform.system() == "Linux": COMMAND = "./ArtGraph.py "
	if platform.system() == "Windows": COMMAND = "ArtGraph.py "
	os.system(COMMAND + str(ID))

DATA = GetArt(ID)
DATA_LOCAL = DATA.copy()

if "P" in ID:
	print("P")
	PID = ID
	while True:
		try:
			ID = StockSetBCode()
			break
		except: True
else: PID = False

ID = int(ID)
appChange = gui("Stock ändern", "800x600", handleArgs=False)
appChange.setBg("#ffffff")
appChange.addLabel("Title", str(ID))

Time = Timestamp()

print("DATA " + str(DATA))
for Entry in EntryList:
    print("Entry " + str(Entry))
    appChange.addLabelEntry(Entry)
    appChange.setEntryChangeFunction(Entry, VerifyInput)
    appChange.setEntry(Entry, DATA[Entry])

    if Entry == "Barcode": appChange.setEntryState(Entry, "disabled")

def StopWindow(btn):
    Debug("StopWindow")
    appChange.stop()

appChange.setStopFunction(VerifyChanges)
appChange.addLabel("Info", "F4 = Grafik anzeigen\nF5 = Speichern und Schliesen")
appChange.bindKey("<F4>", BtnStockGraph)
appChange.bindKey("<F5>", StopWindow)
appChange.go()

