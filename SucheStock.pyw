#!/usr/bin/env python3
from appJar import gui  
from BlueFunc import BlueMkDir, BlueLenDatei, BlueLoad, BlueSave
from debug import Debug
import os
import subprocess
from random import randint
import send
import shutil

EntryList=["Bcode", "Barcode",  "Artikel", "Lieferant", "Name", "Ort", "PreisEK", "PreisVKH", "PreisVK", "Anzahl", "Maschinen"]
EntryList2=["Barcode",  "Artikel", "Lieferant", "Name", "Ort", "PreisEK", "PreisVKH", "PreisVK", "Anzahl", "Maschinen"]
appSuche = gui("Stock Suche", "800x600") 

IDToChange = 0
SearchMaschine = ""

appSuche.addMeter("status"); appSuche.setMeterFill("status", "blue")
appSuche.setMeter("status", 100, text="")

def Maschinen(btn):
	global SearchMaschine
	print("Maschinen")

	MaschinenLaden()

	SearchMaschine = appSuche.openBox(title="Maschinen", dirName="Maschinen/", fileTypes=None, asFile=False).split("/Maschinen/")[1]
	appSuche.setButton("Maschine", SearchMaschine)

	Suche("")

def PrintOrt(btn):
	open("PrintOrt.txt", "w").write(send.StockGetArtInfo("(zkz)Ort", appSuche.getListItems("Suche")[0].split(" | ")[0]).split(" | ")[1])
	try: os.startfile("PrintOrt.txt", "print")
	except: os.system("gedit ./PrintOrt.txt")

def tbFuncSv(btn):
	global IDToChange
	Debug("tbFuncSv")
	for a in EntryList2:
		print(appChange.getEntry(a))
		send.StockSetArtInfo(IDToChange, a, appChange.getEntry(a))
	appChange.stop()
	Delete("")
	appSuche.setEntry("Suche", IDToChange)
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
			appChange.addLabelEntry(EntryList2[x]); appChange.setEntry(EntryList2[x], Data[x+1], callFunction=False)
		
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
		print(Data)
		print(Data)
		for x in range(0, len(EntryList2)):
			appChange.addLabelEntry(EntryList2[x]); appChange.setEntry(EntryList2[x], Data[x+1], callFunction=False)
		
		appChange.addLabel("info", "F5 = Speichern")
		appChange.bindKey("<F5>", tbFuncSv)
		appChange.go()

tools = ["NEU", "ÄNDERN"]
appSuche.addToolbar(tools, tbFunc, findIcon=True)

appSuche.addTickOptionBox("Anzeigen", EntryList2)
appSuche.setOptionBox("Anzeigen", "Name", value=True, callFunction=True)
appSuche.setOptionBox("Anzeigen", "PreisVK", value=True, callFunction=True)
appSuche.setOptionBox("Anzeigen", "Anzahl", value=True, callFunction=True)

appSuche.addLabelEntry("Suche")
#appSuche.addLabelEntry("Bcode")
#appSuche.addLabelEntry("Barcode")
#appSuche.addLabelEntry("Artikel")
appSuche.addLabelEntry("Ort")
appSuche.addNamedButton("Maschine wählen...", "Maschine", Maschinen)
appSuche.addListBox("Suche")

def MaschinenLaden():
	print("MaschinenLaden")
	appSuche.setMeter("status", 0, text="Lade Maschinen")

	try: MaschinenAnzahlIntern = int(BlueLoad("MaschinenAnzahl", "DATA"))
	except: MaschinenAnzahlIntern = 0
	Debug("MaschinenAnzahlIntern : " + str(MaschinenAnzahlIntern))

	MaschinenAnzahlServer = int(send.GetMaschinenAnzahl()); Debug("MaschinenAnzahlServer : " + str(MaschinenAnzahlServer))

	if not MaschinenAnzahlIntern == MaschinenAnzahlServer:

		try: shutil.rmtree("Maschinen")
		except: print("")
		BlueMkDir("Maschinen")		

		Schritt = 100/MaschinenAnzahlServer
		for x in range(MaschinenAnzahlServer):
			appSuche.setMeter("status", appSuche.getMeter("status")[0]*100 + Schritt, text="Lade Maschinen")
			pfade = send.GetMaschine(x)
			for pfad in pfade.split(" "):
				eaThis = "Maschinen"
				for ea in range(0, len(str(pfad).split("/"))):
					eaThis = eaThis + "/" + str(pfad).split("/")[ea]
					if ea + 1 == len(str(pfad).split("/")):
						open(eaThis, "w").write(eaThis)
					else: BlueMkDir(eaThis)
		BlueSave("MaschinenAnzahl", MaschinenAnzahlServer,"DATA")
	
	appSuche.setMeter("status", 100, text="")

def Delete(btn):
	global SearchMaschine
	Debug("Delete")
	#appSuche.setEntry("Bcode", "")
	#appSuche.setEntry("Barcode", "")
	#appSuche.setEntry("Artikel", "")
	appSuche.setEntry("Suche", "")
	appSuche.setEntry("Ort", "")
	SearchMaschine = ""
	appSuche.setButton("Maschine", "Maschine wählen...")

def Suche(btn):
	Debug("Suche")
	appSuche.setMeter("status", 0, text="Suche wird gestartet")
	
	AntwortList=send.SendeSucheStock(appSuche.getEntry("Suche"), appSuche.getEntry("Ort").upper(), SearchMaschine)
	#AntwortList=send.SendeSucheStock(appSuche.getEntry("Bcode"), appSuche.getEntry("Barcode"), appSuche.getEntry("Artikel").lower(), appSuche.getEntry("Ort").upper(), SearchMaschine)
	appSuche.setMeter("status", 10, text="Warte auf daten")
	appSuche.clearListBox("Suche")

	Schritt = (100-10)/(len(AntwortList.split("<K>"))-1); print("Schritt : " + str(Schritt))
	for IDs in AntwortList.split("<K>"):
		if not IDs == "":
			appSuche.setMeter("status", appSuche.getMeter("status")[0]*100 + Schritt, text="Sammle Daten")
			print("status : " + str(appSuche.getMeter("status")[0] + Schritt))
			Linie = str(IDs).rstrip()
			GetThis = ""
			for a in EntryList2:
				if appSuche.getOptionBox("Anzeigen")[a] and not IDs.rstrip() == "":
					GetThis = GetThis + "(zkz)" + str(a)
			Linie = send.StockGetArtInfo(GetThis, IDs)

			appSuche.addListItem("Suche", Linie)
	
	appSuche.setMeter("status", 100, text="")

def StockChange(btn):
	Debug("StockChange")
	IDToChange = appSuche.getListItems("Suche")[0].split(" | ")[0].rstrip()
	Name = "[ " + send.StockGetArtInfo("(zkz)Name", str(IDToChange)) + " ]"
	if btn == "<F1>": # MINUS
		Anzahl = appSuche.numberBox("Anzahl", Name + "\n\nBitte Anzahl eingeben die aus dem Stock entfernt wird : ")
		try:
			send.SendeChangeAnzahl(IDToChange, "-" + str(int(Anzahl)))
			Debug(IDToChange)
			appSuche.infoBox("Stock Geändert", "Sie haben " + str(int(Anzahl)) + "x " + str(Name) + " Entfernt")
			Suche("")
		except: appSuche.infoBox("Error", "Error")
	if btn == "<F2>": # PLUS
		Anzahl = appSuche.numberBox("Anzahl", Name + "\n\nBitte Anzahl eingeben die in Stock gesetzt wird :")
		try:
			send.SendeChangeAnzahl(IDToChange, int(Anzahl))
			Debug(IDToChange)
			appSuche.infoBox("Stock Geändert", "Sie haben " + str(int(Anzahl)) + " zu " + str(Name) + " Hinzugefuegt")
			os.system("")
			Suche("")
		except: appSuche.infoBox("Error", "Error")

appSuche.setFocus("Suche")
MaschinenLaden()
appSuche.addLabel("info", "Enter = Suche \nDelete = Clear\nF1 = Stock MINUS\nF2 = Stock PLUS")
appSuche.addLabel("infoAnzahl", str(send.GetStockZahl()) + " Artikel im Stock")
appSuche.bindKey("<Return>", Suche)
appSuche.bindKey("<F1>", StockChange)
appSuche.bindKey("<F2>", StockChange)
appSuche.bindKey("<F12>", PrintOrt)
appSuche.bindKey("<Delete>", Delete)
appSuche.go()
