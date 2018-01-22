#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from libs.appjar0830 import gui
from libs.send import *
from libs.BlueFunc import *
import os
import sys

def SaveIt():
	print("SaveIt")
	for x in range(0, 10):
		if not appKasse.getOptionBox("Arbeiter") == None:
			if not appKasse.getEntry("e" + str(x)) == "":
				SendeSaveArbeiterLinie(appKasse.getOptionBox("Arbeiter"), "e" + str(x), appKasse.getEntry("e" + str(x)))
			else: SendeSaveArbeiterLinie(appKasse.getOptionBox("Arbeiter"), "e" + str(x), "None")
	return True

def GetArbeiter(btn):
	for x in range(0, 10):
		text = SendeGetArbeiterLinie(appKasse.getOptionBox("Arbeiter"), "e" + str(x))
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
		else: ID = SendeSucheStock(text, "", "").rstrip("<K>")
		
		DATA = StockGetArtInfo(["Name", "Anzahl"], ID).split(" | ")
		print(DATA)
		Name = DATA[1]
		Anzahl = DATA[2]
			

		if Anzahl == "x" or Anzahl == "0":
			appKasse.setEntryInvalid(entryName)
		else:
			appKasse.setEntryValid(entryName)
				
		appKasse.setLabel("l" + str(EntryIndex), ID + " | " + Name + " | Anzahl : " + Anzahl)


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
			Anzahl = Label.split(" | ")[2].replace("Anzahl : ", "")
			if not Anzahl == "x" or Anzahl == "0":
					try:
						SendeChangeAnzahl(ID, "-1")
						appKasse.setEntry("e" + str(EntryName), "")
						appKasse.setLabel("l" + str(EntryName), "")
						#appKasse.infoBox("Stock Geändert", "Sie haben 1x " + str(Name) + " Entfernt")
					except: appKasse.infoBox("Error", "Error: ID " + str(ID))
	SaveIt()
			
appKasse.setStopFunction(SaveIt)
appKasse.addButton("OK", Go)
appKasse.go()
