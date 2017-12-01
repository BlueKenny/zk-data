#!/usr/bin/env python3.6
from libs.appjar0830 import gui
from send import *
from BlueFunc import *

appKasse = gui("Kasse", "600x600")
EntryZahl = 10

if not Date() == BlueLoad("LastUpdate", "DATA")	
	print("Update")

def Verify(entryName):
	print("Verify " + str(entryName))

	text = str(appKasse.getEntry(entryName))
	EntryIndex = int(entryName.replace("e", ""))
	appKasse.setEntryWaitingValidation(entryName)
	appKasse.setLabel("l" + str(EntryIndex), "")

	if len(text) == 13 or len(text) == 6:
		if len(text) == 6: ID = text
		else: ID = SendeSucheStock(text, "", "", "").rstrip("<K>")
		Anzahl = str(StockGetArtInfo("(zkz)Anzahl", ID)).split(" | ")[1]
		Name = str(StockGetArtInfo("(zkz)Name", ID)).split(" | ")[1]
		

		if Anzahl == "x" or Anzahl == "0":
			appKasse.setEntryInvalid(entryName)
		else:
			appKasse.setEntryValid(entryName)
			
		appKasse.setLabel("l" + str(EntryIndex), ID + " | " + Name + " | Anzahl : " + Anzahl)

for EntryName in range(EntryZahl):
	appKasse.addValidationEntry("e" + str(EntryName))
	appKasse.setEntryChangeFunction("e" + str(EntryName), Verify)

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
			

appKasse.addButton("OK", Go)
appKasse.go()
