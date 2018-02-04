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

def VerifyInputFloat(Entry):
    print("VerifyInputFloat")
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


def VerifyInputInt(Entry):
    print("VerifyInputInt")

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

def VerifyInputChar(Entry):
    print("VerifyInputChar")
    print("Verify this input " + str(appChange.getEntry(Entry)))
    appChange.setEntry(Entry, appChange.getEntry(Entry).replace("?", ""))

    if Entry == "Lieferant"
        myString

    if Entry == "Ort":
        myString = appChange.getEntry(Entry).replace(",", ".").upper()
        appChange.setEntry(Entry, myString)

    if Entry == "Artikel" or Entry == "Artikel2" or Entry == "Artikel3" or Entry == "Artikel4":
        myString = appChange.getEntry(Entry).upper()
        EndString = ""
        for character in myString:
            if character.isalpha() or character.isdigit():
                EndString = EndString + str(character)

        appChange.setEntry(Entry, EndString)


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


appChange.addLabelEntry("Name")
appChange.setEntryChangeFunction("Name", VerifyInputChar)
appChange.setEntry("Name", DATA.name)

appChange.addLabelEntry("Artikel")
appChange.setEntryChangeFunction("Artikel", VerifyInputChar)
appChange.setEntry("Artikel", DATA.artikel)

appChange.addLabelEntry("Artikel2")
appChange.setEntryChangeFunction("Artikel2", VerifyInputChar)
appChange.setEntry("Artikel2", DATA.artikel2)

appChange.addLabelEntry("Artikel3")
appChange.setEntryChangeFunction("Artikel3", VerifyInputChar)
appChange.setEntry("Artikel3", DATA.artikel3)

appChange.addLabelEntry("Artikel4")
appChange.setEntryChangeFunction("Artikel4", VerifyInputChar)
appChange.setEntry("Artikel4", DATA.artikel4)

appChange.addLabelEntry("Barcode")
appChange.setEntryChangeFunction("Barcode", VerifyInputInt)
appChange.setEntry("Barcode", DATA.barcode)
appChange.setEntryState("Barcode", "disabled")

appChange.addLabelEntry("Lieferant")
appChange.setEntryChangeFunction("Lieferant", VerifyInputChar)
appChange.setEntry("Lieferant", DATA.lieferant)

appChange.addLabelEntry("Einkaufspreis")
appChange.setEntryChangeFunction("Einkaufspreis", VerifyInputFloat)
appChange.setEntry("Einkaufspreis", DATA.preisek)

appChange.addLabelEntry("Verkaufspreis TVAC")
appChange.setEntryChangeFunction("Verkaufspreis TVAC", VerifyInputFloat)
appChange.setEntry("Verkaufspreis TVAC", DATA.preisvkh)

appChange.addLabelEntry("Verkaufspreis HTVA")
appChange.setEntryChangeFunction("Verkaufspreis HTVA", VerifyInputFloat)
appChange.setEntry("Verkaufspreis HTVA", DATA.preisvk)

appChange.addLabelEntry("Ort")
appChange.setEntryChangeFunction("Ort", VerifyInputChar)
appChange.setEntry("Ort", DATA.ort)

appChange.addLabelEntry("Minimum")
appChange.setEntryChangeFunction("Minimum", VerifyInputFloat)
appChange.setEntry("Minimum", DATA.minimum)


def StopWindow(btn):
    Debug("StopWindow")
    appChange.stop()

appChange.setStopFunction(VerifyChanges)
appChange.addLabel("Info", "F4 = Grafik anzeigen\nF5 = Speichern und Schliesen")
appChange.bindKey("<F4>", BtnStockGraph)
appChange.bindKey("<F5>", StopWindow)
appChange.go()

