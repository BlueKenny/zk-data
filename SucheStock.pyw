#!/usr/bin/env python3.6
from appJar import gui  
from BlueFunc import BlueMkDir, BlueLenDatei, BlueLoad, BlueSave
from debug import Debug
import os
import subprocess
from random import randint
import send

EntryList=["Bcode", "Barcode",  "Artikel", "Lieferant", "Name", "Ort", "PreisEK", "PreisVKH", "PreisVK", "Anzahl"]
appSuche = gui("Stock Suche", "800x600") 

IDToChange = 0

def PrintOrt(btn):
	open("PrintOrt.txt", "w").write(appSuche.getListItems("Suche")[0].split(" | ")[4].rstrip())
	os.startfile("PrintOrt.txt", "print")
def tbFuncSv(btn):
	global IDToChange
	Debug("tbFuncSv")
	for a in EntryList:
		if not a == "Bcode":
			print(appChange.getEntry(a))
			send.StockSetArtInfo(IDToChange, a, appChange.getEntry(a))
	appChange.stop()
	appSuche.setEntry("Bcode", IDToChange)
	Suche("")

def tbFunc(btn):
	global IDToChange
	global appChange
	Debug("btn : " + btn)

	if btn == "NEU":
		Number = appSuche.numberBox("Neu", "Neuer Artike\nBcode n° ?")
		try: print(int(Number))
		except: Number = 800000

		IDToChange = Number
		appChange = gui("Stock Change", "800x600")
		appChange.addLabel("Bcode", str(IDToChange))
		for e in EntryList:
			if not e == "Bcode":
				appChange.addLabelEntry(e)
				appChange.setEntry(e, str(send.StockGetArtInfo(str(IDToChange), e)), callFunction=False)
		appChange.setEntry("Artikel", appSuche.getEntry("Artikel"))
		appChange.addLabel("info", "F5 = Speichern")
		appChange.bindKey("<F5>", tbFuncSv)
		appChange.go()
		
	if btn == "ÄNDERN":
		IDToChange = appSuche.getListItems("Suche")[0].split(" | ")[0].rstrip()
		appChange = gui("Stock Change", "800x600")
		appChange.addLabel("Bcode", str(IDToChange))
		for e in EntryList:
			if not e == "Bcode":
				appChange.addLabelEntry(e)
				appChange.setEntry(e, str(send.StockGetArtInfo(str(IDToChange), e)), callFunction=False)
		
		appChange.addLabel("info", "F5 = Speichern")
		appChange.bindKey("<F5>", tbFuncSv)
		appChange.go()

tools = ["NEU", "ÄNDERN"]
appSuche.addToolbar(tools, tbFunc, findIcon=True)

appSuche.addLabelEntry("Bcode")
appSuche.addLabelEntry("Barcode")
appSuche.addLabelEntry("Artikel")
appSuche.addLabelEntry("Ort")
appSuche.addListBox("Suche")

def Delete(btn):
	Debug("Delete")
	appSuche.setEntry("Bcode", "")
	appSuche.setEntry("Barcode", "")
	appSuche.setEntry("Artikel", "")
	appSuche.setEntry("Ort", "")

def Suche(btn):
	Debug("Suche")
	appSuche.setLabel("infoAnzahl", str(send.GetStockZahl()) + " Artikel im Stock")
	AntwortList=send.SendeSucheStock(appSuche.getEntry("Bcode"), appSuche.getEntry("Barcode"), appSuche.getEntry("Artikel").lower(), appSuche.getEntry("Ort").upper())
	appSuche.clearListBox("Suche")
	for Linien in AntwortList.split("<K>"):
		if not Linien == "":
			appSuche.addListItem("Suche", Linien)
			bcode=Linien.split(" | ")[0]
			artikel=Linien.split(" | ")[1]

def StockChange(btn):
	Debug("StockChange")
	IDToChange = appSuche.getListItems("Suche")[0].split(" | ")[0].rstrip()
	Name = appSuche.getListItems("Suche")[0].split(" | ")[3].rstrip()
	if btn == "<F1>": # MINUS
		Anzahl = appSuche.numberBox("Anzahl", Name + "\n\nBitte Anzahl eingeben die aus dem Stock entfernt wird : ")
		try:
			send.SendeChangeAnzahl(IDToChange, "-" + str(int(Anzahl)))
			Debug(IDToChange)
			appSuche.infoBox("Stock Geändert", "Sie haben " + str(int(Anzahl)) + "x " + str(IDToChange) + " Entfernt")
			Suche("")
		except: appSuche.infoBox("Error", "Error")
	if btn == "<F2>": # PLUS
		Anzahl = appSuche.numberBox("Anzahl", Name + "\n\nBitte Anzahl eingeben die in Stock gesetzt wird :")
		try:
			send.SendeChangeAnzahl(IDToChange, int(Anzahl))
			Debug(IDToChange)
			appSuche.infoBox("Stock Geändert", "Sie haben " + str(int(Anzahl)) + " zu " + str(IDToChange) + " Hinzugefuegt")
			os.system("")
			Suche("")
		except: appSuche.infoBox("Error", "Error")
	

appSuche.addLabel("info", "Enter = Suche \nDelete = Clear\nF1 = Stock MINUS\nF2 = Stock PLUS")
appSuche.addLabel("infoAnzahl", "0" + " Artikel im Stock")
appSuche.bindKey("<Return>", Suche)
appSuche.bindKey("<F1>", StockChange)
appSuche.bindKey("<F2>", StockChange)
appSuche.bindKey("<F12>", PrintOrt)
appSuche.bindKey("<Delete>", Delete)
appSuche.go()
