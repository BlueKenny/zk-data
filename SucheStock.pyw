#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
if not os.path.exists("/home"):
	os.system("git pull")

from libs.appjar0830 import gui  
from libs.BlueFunc import *
from libs.debug import Debug
import platform
from libs.send import *
from libs.barcode import *
import csv

from libs.CheckConf import *

EntryList=["Barcode", "Artikel", "Artikel2", "Artikel3", "Lieferant", "Name", "Ort", "PreisEK", "PreisVKH", "PreisVK", "Anzahl"]
appSuche = gui("Search Stock", "800x650") 
appSuche.setBg("#ffffff")

IDToChange = 0

appSuche.addMeter("status"); appSuche.setMeterFill("status", "blue")
appSuche.setMeter("status", 100, text="")

#NEWS
NEWS_INDEX = BlueLoad("NEWS_INDEX", "DATA/DATA")
if NEWS_INDEX == None: NEWS_INDEX = 20
NEWS_INDEX = int(NEWS_INDEX)
with codecs.open("news.csv", "r", "utf-8") as csvfile:
	reader = csv.reader(csvfile, delimiter=":", quotechar="\"")
	for eachLine in reader:
		if not "INDEX" in eachLine and NEWS_INDEX < int(eachLine[0]):
			print(eachLine)
			NEWS_INDEX = int(eachLine[0])
			appSuche.infoBox("Update " + eachLine[0], eachLine[1] + "\n\n" + eachLine[3], parent=None)
BlueSave("NEWS_INDEX", NEWS_INDEX, "DATA/DATA")

def BtnStockGraph(btn):
	ID = appSuche.getListItems("Suche")[0].split(" | ")[0]

	if platform.system() == "Linux": COMMAND = "./ArtGraph.py "
	if platform.system() == "Windows": COMMAND = "ArtGraph.py "
	os.system(COMMAND + str(ID))
	
def BtnPrintBarcode(btn):
	ID = appSuche.getListItems("Suche")[0].split(" | ")[0]
	print("ID " + str(ID))
	
	GetData = StockGetArtInfo(["Barcode", "Name", "PreisVK"], ID).split(" | ")
	print("GetData " + str(GetData))

	Anzahl = appSuche.numberBox("Drucken", "Welche Anzahl soll gedruckt werden?")
	for a in range(0, Anzahl):
		PrintBarcode("", GetData[0], GetData[1], GetData[2], GetData[3])

def BtnPrintOrt(btn):
	PrintLocation(StockGetArtInfo(["Ort"], appSuche.getListItems("Suche")[0].split(" | ")[0]).split(" | ")[1])


appSuche.addLabelEntry("Suche")
appSuche.addLabelEntry("Ort")
appSuche.addLabelEntry("Lieferant")
ListBoxSuche = appSuche.addListBox("Suche")
ListBoxSuche.bind("<Double-1>", lambda *args: tbFunc("ÄNDERN"))# if List Item double click then change

def tbFunc(btn):
	global IDToChange
	global appChange
	Debug("btn : " + btn)

	if btn == "NEU":
		if platform.system() == "Linux": COMMAND = "./ChangeStock.pyw"
		if platform.system() == "Windows": COMMAND = "ChangeStock.pyw"
		application = os.popen(COMMAND).readlines()
		Suche(BlueLoad("LastID", "DATA/DATA"))
		
	if btn == "ÄNDERN":
		ID = appSuche.getListBox("Suche")[0].split(" | ")[0]
		if platform.system() == "Linux": COMMAND = "./ChangeStock.pyw"
		if platform.system() == "Windows":  COMMAND = "ChangeStock.pyw"
		application = os.popen(COMMAND + " " + ID).readlines()
		Suche(BlueLoad("LastID", "DATA/DATA"))

tools = ["NEU", "ÄNDERN"]
appSuche.addToolbar(tools, tbFunc, findIcon=False)

#appSuche.addTickOptionBox("Anzeigen", EntryList)

#for each in EntryList:#try:
#	print(appSuche.getOptionBox("Anzeigen")[each])
#	appSuche.setOptionBox("Anzeigen", each, value=True, callFunction=True)
	#for eachAnzeigenOption in BlueLoad("Anzeigen-Stock", "DATA/DATA").split("/"):
	#	print(eachAnzeigenOption + " is True")
	#	print(EntryList[int(eachAnzeigenOption)])
	#	appSuche.setOptionBox("Anzeigen", str(EntryList[int(eachAnzeigenOption)]), value=True, callFunction=True)
#except: print("Anzeigen nicht gefunden")

def Delete(btn):
	Debug("Delete")
	appSuche.setEntry("Suche", "")
	appSuche.setEntry("Ort", "")
	appSuche.setEntry("Lieferant", "")
	appSuche.setFocus("Suche")

def Suche(btn):
    Debug("Suche")
    if len(btn) == 6:
        try:
            ID = int(btn)
            appSuche.setEntry("Suche", str(ID))
        except: True

    appSuche.setMeter("status", 0, text="Suche wird gestartet")

    Suche = appSuche.getEntry("Suche").replace(" ", "")
    Ort = appSuche.getEntry("Ort").upper()
    Lieferant = appSuche.getEntry("Lieferant").lower()

    if Suche == "" and Ort == "" and Lieferant == "":
        NichtSuchen = True
    else:
        NichtSuchen = False

    if not NichtSuchen:
        AntwortList=SendeSucheStock(Suche, Ort, Lieferant)


        appSuche.setMeter("status", 10, text="Warte auf daten")
        appSuche.clearListBox("Suche")

        if btn == "first":
            AntwortList = AntwortList.split("<K>")[0]
            Schritt = (100-10)/(1); print("Schritt " + str(Schritt))
        else:
            Schritt = (100-10)/(len(AntwortList.split("<K>"))-1); print("Schritt " + str(Schritt))

        for IDs in AntwortList.split("<K>"):
            Debug("Get Info for ID " + str(IDs))
            if not IDs == "" and not IDs == "0"and not IDs == None and not IDs == "None":
                appSuche.setMeter("status", appSuche.getMeter("status")[0] * 100 + Schritt, text="Lade Daten")
                print(" " + str(appSuche.getMeter("status")[0] + Schritt))
                Linie = str(IDs).rstrip()
                Linie = StockGetArtInfo(["Artikel", "Lieferant", "Name", "Ort", "PreisVK", "Anzahl"], IDs)

                appSuche.addListItem("Suche", Linie)
                if "P" in IDs:
                    appSuche.setListItemBg("Suche", Linie, "#FFF68F")
                else:
                    appSuche.setListItemBg("Suche", Linie, "#ffffff")
        appSuche.selectListItemAtPos("Suche", 0, callFunction=False)
    appSuche.setLabel("infoAnzahl",  str(GetStockZahl() + " Artikel zu verfügung"))
    appSuche.setMeter("status", 100, text="")

def StockChange(btn):
	Debug("StockChange")
	IDToChange = appSuche.getListBox("Suche")[0].split(" | ")[0].rstrip()
	if not "P" in IDToChange:
		Name = "[ " + StockGetArtInfo(["Name"], str(IDToChange)) + " ]"
		if btn == "<F1>": # MINUS
			Anzahl = appSuche.numberBox("Entfernen", "Wie viele wolen sie ENTFERNEN ?")
			try:
				SendeChangeAnzahl(IDToChange, "-" + str(int(Anzahl)))
				Debug(IDToChange)
				appSuche.infoBox("Gespeichert", "Anzahl wurde geändert")
				appSuche.setEntry("Suche", IDToChange)
				Suche("first")
			except: appSuche.infoBox("Fehler", "Fehler")
		if btn == "<F2>": # PLUS
			Anzahl = appSuche.numberBox("Hinzufügen", "Wie viele wollen sie HINZUFUGEN ?")
			try:
				SendeChangeAnzahl(IDToChange, int(Anzahl))
				Debug(IDToChange)
				appSuche.infoBox("Gespeichert", "Anzahl wurde geändert")
				appSuche.setEntry("Suche", IDToChange)
				Suche("first")
			except: appSuche.infoBox("Fehler", "Fehler")

appSuche.setFocus("Suche")
appSuche.addLabel("KeyEnter", "Enter = Suchen")
appSuche.addLabel("KeyDelete", "Entfernen = Alle fehler leeren")
appSuche.addLabel("space0", "")
appSuche.addLabel("KeyF1", "F1 = Artikel entfernen")
appSuche.addLabel("KeyF2", "F2 = Artikel hinzufügen")
appSuche.addLabel("KeyF11", "F11 = Ort drucken")
appSuche.addLabel("KeyF12", "F12 = Drucken")
appSuche.addLabel("space1", "")

#appSuche.translate("TextKeyEnter", "Enter = Article search")
#appSuche.translate("TextKeyDelete", "Delete = Clear all searches")
#appSuche.translate("TextKeyF1", "F1 = remove article")
#appSuche.translate("TextKeyF2", "F2 = add article")
#appSuche.translate("TextKeyF11", "F11 = print location")
#appSuche.translate("TextKeyF12", "F12 = print barcode")

appSuche.addLabel("infoAnzahl",  str(GetStockZahl()) + " Artikel zu verfügung")
appSuche.bindKey("<Return>", Suche)
appSuche.bindKey("<F1>", StockChange)
appSuche.bindKey("<F2>", StockChange)
appSuche.bindKey("<F4>", BtnStockGraph)
appSuche.bindKey("<F11>", BtnPrintOrt)
appSuche.bindKey("<F12>", BtnPrintBarcode)
appSuche.bindKey("<Delete>", Delete)

appSuche.go()
