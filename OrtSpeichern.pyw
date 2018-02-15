#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from libs.appjar0830 import gui
from libs.send import *
from libs.BlueFunc import *
from libs.barcode import *
import os

appKasse = gui("Ort", "600x600")	

ID = 0
def PrintOrt(btn):
	Data = StockGetArtInfo(["Barcode", "Name", "PreisVK"], ID).split(" | ")
	PrintBarcode("", ID, Data[1], Data[2], Data[3])
		
def Verify(entryName):
	global ID
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
		Data = StockGetArtInfo(["Anzahl", "Name", "Ort"], ID).split(" | ")
		Anzahl = Data[1]
		Name = Data[2]
		Ort = Data[3]

		if Name == "x":
			appKasse.setEntryInvalid(entryName)
		else:
			appKasse.setEntryValid(entryName)
					
		appKasse.setLabel("lBCode", ID)
		appKasse.setLabel("lName", Name)
		appKasse.setEntry("Ort", Ort)

def NextFocus(btn):
	print("nextFocus")
	if btn == "e1": appKasse.setFocus("Ort")
	if btn == "Ort":
		appKasse.setFocus("e1")
		Go("")

appKasse.addLabel("infoBCode", "BCode / Barcode :")
appKasse.addValidationEntry("e1")
appKasse.setEntryChangeFunction("e1", Verify)
appKasse.setFocus("e1")
appKasse.setEntrySubmitFunction("e1", NextFocus)

appKasse.addLabel("lBCode", "")
appKasse.addLabel("lName", "")

appKasse.addLabelEntry("Ort")
appKasse.setEntrySubmitFunction("Ort", NextFocus)

def Delete(btn):
	Debug("Delete")
	appKasse.setEntry("e1", "")
	appKasse.setFocus("e1")

def Go(btn):
	print("Go ")

	Name = appKasse.getLabel("lName")
	if not Name == "x":
		ID = appKasse.getLabel("lBCode")
		StockSetArtInfo(ID, "Ort", appKasse.getEntry("Ort"))
		#appKasse.infoBox("Gespeichert", "Ort gespeichert \n ID " + str(ID))
		appKasse.setFocus("e1")
		appKasse.setEntry("e1", "")

	else: appKasse.infoBox("Error", "Error: ID " + str(ID))
			

appKasse.addButton("OK", Go)
appKasse.addButton("Ort Drucken", PrintOrt)
appKasse.bindKey("<Delete>", Delete)
appKasse.bindKey("<F12>", PrintOrt)

appKasse.go()
