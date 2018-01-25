#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from libs.appjar0830 import gui
from libs.send import *
from libs.BlueFunc import *
import os
import sys

LastWorker = ""

def SaveIt():
	print("SaveIt")
	print("LastWorker: " + str(LastWorker))
	for x in range(0, 10):
		if not LastWorker == None and not LastWorker == "":
			if not appKasse.getEntry("e" + str(x)) == "":
				SendeSaveArbeiterLinie(LastWorker, "e" + str(x), appKasse.getEntry("e" + str(x)))
			else: SendeSaveArbeiterLinie(LastWorker, "e" + str(x), "None")
	return True

def GetArbeiter(btn):
    global LastWorker
    SaveIt()
    LastWorker = appKasse.getOptionBox("Arbeiter")
    for x in range(0, 10):
        text = SendeGetArbeiterLinie(LastWorker, "e" + str(x))
        if not text == "None":
            appKasse.setEntry("e" + str(x), text)
        else: appKasse.setEntry("e" + str(x), "")
    appKasse.setFocus("e0")


appKasse = gui("Kasse", "600x600")
EntryZahl = 10

ListeDerArbeiter=sorted(GetListeDerArbeiter().split("|"))
appKasse.addLabelOptionBox("Arbeiter", ListeDerArbeiter)
appKasse.setOptionBoxSubmitFunction("Arbeiter", GetArbeiter) 

def Verify(entryName):
    print("Verify " + str(entryName))


    text = str(appKasse.getEntry(entryName))
    EntryIndex = int(entryName.replace("e", ""))
    appKasse.setEntryWaitingValidation(entryName)
    appKasse.setLabel("l" + str(EntryIndex), "")

    if len(text) == 13 or len(text) == 6:
        if len(text) == 6: ID = text
        else: ID = SendeSucheStock(text, "", "").split("<K>")[0]
		
        DATA = StockGetArtInfo(["Name", "Ort", "PreisVK", "Anzahl"], ID).split(" | ")
        print(DATA)
        Name = DATA[1]
        Ort = DATA[2]
        Preis = DATA[3]
        Anzahl = int(DATA[4])
			

        if Anzahl < 1:
            appKasse.setEntryInvalid(entryName)
        else:
            appKasse.setEntryValid(entryName)
				
        appKasse.setLabel("l" + str(EntryIndex), ID + " | " + str(Name) + " | Ort : " + str(Ort) + " | Preis : " + str(Preis) + " | Anzahl : " + str(Anzahl))


def NextFocus(entry):
    print("NextFocus")
    EntryID = int(entry.replace("e", ""))
    if EntryID == 9: EntryID = -1
    NextEntry = "e" + str(EntryID + 1)
    appKasse.setFocus(NextEntry)

for EntryName in range(EntryZahl):
    appKasse.addValidationEntry("e" + str(EntryName))
    appKasse.setEntryChangeFunction("e" + str(EntryName), Verify)
    appKasse.setEntrySubmitFunction("e" + str(EntryName), NextFocus)
    appKasse.addLabel("l" + str(EntryName), "")


def Go(btn):
    print("Go ")
    for EntryName in range(EntryZahl):
        Label = appKasse.getLabel("l" + str(EntryName))
        if not Label == "":
            ID = Label.split(" | ")[0]
            Name = Label.split(" | ")[1]
            Anzahl = int(Label.split(" | ")[4].replace("Anzahl : ", ""))
            if not Anzahl < 1:
                try:
                    SendeChangeAnzahl(ID, "-1")
                    appKasse.setEntry("e" + str(EntryName), "")
                    appKasse.setLabel("l" + str(EntryName), "")
                    #appKasse.infoBox("Stock Geändert", "Sie haben 1x " + str(Name) + " Entfernt")
                except: appKasse.infoBox("Error", "Error: ID " + str(ID))
            else: appKasse.infoBox("Achtung", str(Name) + "\n\nAnzahl ist ungültig")
    SaveIt()
			
appKasse.setStopFunction(SaveIt)
appKasse.setFocus("e0")
appKasse.addButton("OK", Go)
appKasse.go()
