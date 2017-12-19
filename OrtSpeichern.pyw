#!/usr/bin/env python3
from libs.appjar0830 import gui
from send import *
from BlueFunc import *
import os

if not Date() == BlueLoad("LastUpdate", "DATA"):
	if os.path.exists("/home"): os.system("./Updater.pyw")
	else: os.system("Updater.pyw")

appKasse = gui("Ort", "600x600")	

def PrintOrt(btn):
	open("PrintOrt.txt", "w").write(StockGetArtInfo("(zkz)Ort", appKasse.getLabel("lBCode")).split(" | ")[1])
	try: os.startfile("PrintOrt.txt", "print")
	except: os.system("gedit ./PrintOrt.txt")
		
def Verify(entryName):
	print("Verify " + entryName)

	text = str(appKasse.getEntry(entryName))
	print(text)
	EntryIndex = int(entryName.replace("e", ""))
	appKasse.setEntryWaitingValidation(entryName)

	appKasse.setLabel("lBCode", "")
	appKasse.setLabel("lName", "")
	appKasse.setEntry("Ort", "")

	if len(text) == 13 or len(text) == 6:
		if len(text) == 6: ID = text
		else: ID = SendeSucheStock(text, "", "").rstrip("<K>")
		Anzahl = str(StockGetArtInfo("(zkz)Anzahl", ID)).split(" | ")[1]
		Name = str(StockGetArtInfo("(zkz)Name", ID)).split(" | ")[1]
		Ort = str(StockGetArtInfo("(zkz)Ort", ID)).split(" | ")[1]

		if Name == "x":
			appKasse.setEntryInvalid(entryName)
		else:
			appKasse.setEntryValid(entryName)
					
		appKasse.setLabel("lBCode", ID)
		appKasse.setLabel("lName", Name)
		appKasse.setEntry("Ort", Ort)



appKasse.addLabel("infoBCode", "BCode / Barcode :")
appKasse.addValidationEntry("e1")
appKasse.setEntryChangeFunction("e1", Verify)

appKasse.addLabel("lBCode", "")
appKasse.addLabel("lName", "")

appKasse.addLabelEntry("Ort")

def Delete(btn):
	Debug("Delete")
	appKasse.setEntry("e1", "")

def Go(btn):
	print("Go ")

	Name = appKasse.getLabel("lName")
	if not Name == "x":
		ID = appKasse.getLabel("lBCode")
		StockSetArtInfo(ID, "Ort", appKasse.getEntry("Ort"))
		appKasse.infoBox("Gespeichert", "Ort gespeichert \n ID " + str(ID))


	else: appKasse.infoBox("Error", "Error: ID " + str(ID))
			

appKasse.addButton("OK", Go)
appKasse.addButton("Ort Drucken", PrintOrt)
appKasse.bindKey("<Delete>", Delete)
appKasse.bindKey("<F12>", PrintOrt)

appKasse.go()
