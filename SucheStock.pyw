#!/usr/bin/env python3.6
from appJar import gui  
from BlueFunc import BlueMkDir, BlueLenDatei, BlueLoad, BlueSave
from debug import Debug
import os
import subprocess
from random import randint
import send

EntryList=["Bcode", "Barcode",  "Artikel", "Lieferant", "Name", "Ort", "PreisEK", "PreisVKH", "PreisVK", "Anzahl"]
EntryList2=["Barcode",  "Artikel", "Lieferant", "Name", "Ort", "PreisEK", "PreisVKH", "PreisVK", "Anzahl"]
appSuche = gui("Stock Suche", "800x600") 

IDToChange = 0
SearchMachine = ""

def Machinen(btn):
	global SearchMachine
	print("Machinen")
	SearchMachine = appSuche.openBox(title="Machinen", dirName="Machinen/", fileTypes=None, asFile=False).split("/Machinen/")[1]
	appSuche.setButton("Machine", SearchMachine)

def PrintOrt(btn):
	open("PrintOrt.txt", "w").write(send.StockGetArtInfo("(zkz)Ort", appSuche.getListItems("Suche")[0].split(" | ")[0]).split(" | ")[1])
	try: os.startfile("PrintOrt.txt", "print")
	except: os.system("gedit ./PrintOrt.txt")

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
		GetThis = ""
		for a in EntryList2:
			GetThis = GetThis + "(zkz)" + str(a)
		Data = send.StockGetArtInfo(GetThis, str(IDToChange)).split(" | ")
		for x in range(0, len(EntryList2)):
			appChange.addLabelEntry(EntryList2[x]); appChange.setEntry(EntryList2[x], Data[x + 1], callFunction=False)
		
		appChange.addLabel("info", "F5 = Speichern")
		appChange.bindKey("<F5>", tbFuncSv)
		appChange.go()
		
	if btn == "ÄNDERN":
		IDToChange = appSuche.getListItems("Suche")[0].split(" | ")[0].rstrip()
		appChange = gui("Stock Change", "800x600")
		appChange.addLabel("Bcode", str(IDToChange))
		GetThis = ""
		for a in EntryList2:
			GetThis = GetThis + "(zkz)" + str(a)
		Data = send.StockGetArtInfo(GetThis, str(IDToChange)).split(" | ")
		for x in range(0, len(EntryList2)):
			appChange.addLabelEntry(EntryList2[x]); appChange.setEntry(EntryList2[x], Data[x + 1], callFunction=False)
		
		appChange.addLabel("info", "F5 = Speichern")
		appChange.bindKey("<F5>", tbFuncSv)
		appChange.go()

tools = ["NEU", "ÄNDERN"]
appSuche.addToolbar(tools, tbFunc, findIcon=True)

appSuche.addTickOptionBox("Anzeigen", EntryList2)
appSuche.setOptionBox("Anzeigen", "Name", value=True, callFunction=True)
appSuche.setOptionBox("Anzeigen", "PreisVK", value=True, callFunction=True)
appSuche.setOptionBox("Anzeigen", "Anzahl", value=True, callFunction=True)

appSuche.addLabelEntry("Bcode")
appSuche.addLabelEntry("Barcode")
appSuche.addLabelEntry("Artikel")
appSuche.addLabelEntry("Ort")
appSuche.addNamedButton("Machine wählen...", "Machine", Machinen)
appSuche.addListBox("Suche")

def Delete(btn):
	Debug("Delete")
	appSuche.setEntry("Bcode", "")
	appSuche.setEntry("Barcode", "")
	appSuche.setEntry("Artikel", "")
	appSuche.setEntry("Ort", "")
	SearchMachine = ""
	appSuche.setButton("Machine", "Machine wählen...")

def Suche(btn):
	Debug("Suche")
	appSuche.setLabel("infoAnzahl", str(send.GetStockZahl()) + " Artikel im Stock")
	
	AntwortList=send.SendeSucheStock(appSuche.getEntry("Bcode"), appSuche.getEntry("Barcode"), appSuche.getEntry("Artikel").lower(), appSuche.getEntry("Ort").upper(), SearchMachine)
	appSuche.clearListBox("Suche")
	for IDs in AntwortList.split("<K>"):
		if not IDs == "":
			Linie = str(IDs).rstrip()
			GetThis = ""
			for a in EntryList2:
				if appSuche.getOptionBox("Anzeigen")[a] and not IDs.rstrip() == "":
					GetThis = GetThis + "(zkz)" + str(a)
			Linie = send.StockGetArtInfo(GetThis, IDs)

			appSuche.addListItem("Suche", Linie)

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
