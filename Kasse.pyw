#!/usr/bin/env python3.6
from appJar import gui
from send import *

appKasse = gui("Kasse", "500x500")
EntryZahl = 10

def Verify(btn):
	OK = True
	for EntryName in range(EntryZahl):
		entryName = "e" + str(EntryName)
		text = str(appKasse.getEntry(entryName))
		appKasse.setEntryWaitingValidation(entryName)
		if len(text) == 12 or len(text) == 13:
			ID = SendeSucheStock(text, "", "").rstrip("<K>")
			Anzahl = str(StockGetArtInfo("(zkz)Anzahl", ID)).split(" | ")[1]
			if Anzahl == "x":
				appKasse.setEntryInvalid(entryName)
				OK = False
			else:
				appKasse.setEntryValid(entryName)
				if Anzahl == "0": appKasse.infoBox("Achtung", "[" + str(StockGetArtInfo("(zkz)Name", ID)).split(" | ")[1] + "] ist schon nicht mehr im Stock")


for EntryName in range(EntryZahl):
	appKasse.addValidationEntry("e" + str(EntryName))
	appKasse.setEntryMaxLength("e" + str(EntryName), 13)
	#appKasse.setEntryChangeFunction("e" + str(EntryName), Verify)
appKasse.addButton("OK", Verify)

appKasse.go()
