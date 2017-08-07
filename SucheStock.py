#!/usr/bin/env python3.6
from appJar import gui  
from BlueFunc import BlueMkDir, BlueLenDatei, BlueLoad, BlueSave
from debug import Debug
import os
import subprocess
from random import randint
# Lieferant
EntryList=["Bcode", "Artikel", "Name", "Ort", "PreisEK", "PreisVKH", "PreisVK", "Anzahl"]
appSuche = gui("Stock Suche", "800x600") 

def FuncSave(btn):
	Debug("FuncSave")
	for a in EntryList:
		if not a == "Bcode":
			BlueSave(a, appSuche.getEntry(a), datei)


def FuncSuche(btn):
	global datei
	Debug("FuncSuche")
	BcodeSuche = appSuche.getEntry("Bcode")
	Debug("BcodeSuche : " + str(BcodeSuche))
	if len(BcodeSuche) == 6 and int(BcodeSuche):
		pfad = "stock/" + BcodeSuche[-3] + BcodeSuche[-2] + BcodeSuche[-1] + "/"
		Debug("pfad : " + str(pfad))
		BlueMkDir(pfad)
		datei = pfad + BcodeSuche
		if os.path.exists(datei):
			Debug("Laden")
			for x in EntryList:
				if not x == "Bcode":
					appSuche.setEntry(x, BlueLoad(x, datei))
		else:
			Debug("Neu")
			for x in EntryList:
				if not x == "Bcode":
					appSuche.setEntry(x, "")




for EntryText in EntryList:
	if EntryText == "Bcode":
		appSuche.addLabelEntry(EntryText)
		appSuche.addButton("Suche", FuncSuche)
	else: 
		appSuche.addLabelEntry(EntryText)

appSuche.bindKey("<Return>", FuncSave)
appSuche.go()
