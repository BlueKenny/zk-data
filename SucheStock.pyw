#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
if not os.path.exists("/home"):
	os.system("git pull")

from libs.appjar0830 import gui  
from libs.BlueFunc import *
from libs.debug import Debug
import subprocess
from random import randint
from libs.send import *
from libs.barcode import *
import csv

from libs.CheckConf import *

EntryList=["Barcode", "Artikel", "Lieferant", "Name", "Ort", "PreisEK", "PreisVKH", "PreisVK", "Anzahl"]
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

	if os.path.exists("/home"):
		COMMAND = "./ArtGraph.py "
	else: COMMAND = "ArtGraph.py "
	os.system(COMMAND + str(ID))
	
def BtnPrintBarcode(btn):
	ID = appSuche.getListItems("Suche")[0].split(" | ")[0]
	print("ID " + str(ID))
	
	GetData = StockGetArtInfo(["Barcode", "Name", "PreisVK"], ID).split(" | ")
	print("GetData " + str(GetData))

	Anzahl = appSuche.numberBox("QuantityToPrint", "Quantity to print")
	for a in range(0, Anzahl):
		PrintBarcode("", GetData[0], GetData[1], GetData[2], GetData[3])

def BtnPrintOrt(btn):
	PrintLocation(StockGetArtInfo(["Ort"], appSuche.getListItems("Suche")[0].split(" | ")[0]).split(" | ")[1])


appSuche.addLabelEntry("Search")
appSuche.addLabelEntry("Location")
appSuche.addLabelEntry("Supplier")
ListBoxSuche = appSuche.addListBox("Suche")
ListBoxSuche.bind("<Double-1>", lambda *args: tbFunc("CHANGE"))# if List Item double click then change

def tbFunc(btn):
	global IDToChange
	global appChange
	Debug("btn : " + btn)

	if btn == "NEW":
		if os.path.exists("/home"):
			COMMAND = "./ChangeStock.pyw"
		else: COMMAND = "ChangeStock.pyw"
		application = os.popen(COMMAND).readlines()
		Suche(BlueLoad("LastID", "DATA/DATA"))
		
	if btn == "CHANGE":
		ID = appSuche.getListBox("Suche")[0].split(" | ")[0]
		if os.path.exists("/home"):
			COMMAND = "./ChangeStock.pyw"
		else: COMMAND = "ChangeStock.pyw"
		application = os.popen(COMMAND + " " + ID).readlines()
		LookAt = application[-1].rstrip()
		Suche(BlueLoad("LastID", "DATA/DATA"))

tools = ["NEW", "CHANGE"]
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
	appSuche.setEntry("Search", "")
	appSuche.setEntry("Location", "")
	appSuche.setEntry("Supplier", "")
	appSuche.setFocus("Search")

def Suche(btn):
	Debug("Suche")
	if len(btn) == 6:
		try:
			ID = int(btn)
			appSuche.setEntry("Search", str(ID))
		except: True

	appSuche.setMeter("status", 0, text=appSuche.translate("TextStartSearch", "Start searching"))
	
	AntwortList=SendeSucheStock(appSuche.getEntry("Search").replace(" ", ""), appSuche.getEntry("Location").upper(), appSuche.getEntry("Supplier").lower())


	appSuche.setMeter("status", 10, text=appSuche.translate("TextWaitingForData", "Waiting for data"))
	appSuche.clearListBox("Suche")

	if btn == "first":
		AntwortList = AntwortList.split("<K>")[0]
		Schritt = (100-10)/(1); print(appSuche.translate("TextStep", "Step") + " " + str(Schritt))
	else:
		Schritt = (100-10)/(len(AntwortList.split("<K>"))-1); print(appSuche.translate("TextStep", "Step") + " " + str(Schritt))

	for IDs in AntwortList.split("<K>"):
		Debug("Get Info for ID " + str(IDs))
		if not IDs == "" and not IDs == "0"and not IDs == None and not IDs == "None":
			appSuche.setMeter("status", appSuche.getMeter("status")[0]*100 + Schritt, text=appSuche.translate("TextQueryData", "Get Data"))
			print(appSuche.translate("TextStatus", "Status") + " " + str(appSuche.getMeter("status")[0] + Schritt))
			Linie = str(IDs).rstrip()
			Linie = StockGetArtInfo(["Artikel", "Lieferant", "Name", "Ort", "PreisVK", "Anzahl"], IDs)

			appSuche.addListItem("Suche", Linie)
			if "P" in IDs:
				appSuche.setListItemBg("Suche", Linie, "#FFF68F")
			else:
				appSuche.setListItemBg("Suche", Linie, "#ffffff")
	appSuche.selectListItemAtPos("Suche", 0, callFunction=False)
	appSuche.setLabel("infoAnzahl",  str(GetStockZahl() + " " + appSuche.translate("TextArticleInStock", "Article in stock")))
	appSuche.setMeter("status", 100, text="")

def SaveIt():
	Debug("SaveIt")
	#PosInList = 0
	#for each in appSuche.getOptionBox("Anzeigen"):
	#	value = appSuche.getOptionBox("Anzeigen")[each]
	#	if value:
	#		print(each + " = " + str(PosInList) + " is True")
	#		try: AnzeigenListe = AnzeigenListe + "/" + str(PosInList)
	#		except: AnzeigenListe = str(PosInList)
	#	PosInList = PosInList + 1
	#try: BlueSave("Anzeigen-Stock", AnzeigenListe, "DATA/DATA")
	#except: BlueSave("Anzeigen-Stock", "0/1/2", "DATA/DATA")

	return True

def StockChange(btn):
	Debug("StockChange")
	IDToChange = appSuche.getListBox("Suche")[0].split(" | ")[0].rstrip()
	if not "P" in IDToChange:
		Name = "[ " + StockGetArtInfo(["Name"], str(IDToChange)) + " ]"
		if btn == "<F1>": # MINUS
			Anzahl = appSuche.numberBox("QuantityToRemove", "Quantity to remove")
			try:
				SendeChangeAnzahl(IDToChange, "-" + str(int(Anzahl)))
				Debug(IDToChange)
				appSuche.infoBox("QuantityChanged", "Quantity Changed")
				appSuche.setEntry("Search", IDToChange)
				Suche("first")
			except: appSuche.infoBox("Error", "Error")
		if btn == "<F2>": # PLUS
			Anzahl = appSuche.numberBox("QuantityToAdd", "Quantity to add")
			try:
				SendeChangeAnzahl(IDToChange, int(Anzahl))
				Debug(IDToChange)
				appSuche.infoBox("QuantityChanged", "Quantity Changed")
				appSuche.setEntry("Search", IDToChange)
				Suche("first")
			except: appSuche.infoBox("Error", "Error")

appSuche.setFocus("Search")
appSuche.addLabel("InfoKeyEnter", "")
appSuche.addLabel("InfoKeyDelete", "")
appSuche.addLabel("InfoKeyF1", "")
appSuche.addLabel("InfoKeyF2", "")
appSuche.addLabel("InfoKeyF11", "")
appSuche.addLabel("InfoKeyF12", "")
appSuche.addLabel("space", "")

#appSuche.translate("TextKeyEnter", "Enter = Article search")
#appSuche.translate("TextKeyDelete", "Delete = Clear all searches")
#appSuche.translate("TextKeyF1", "F1 = remove article")
#appSuche.translate("TextKeyF2", "F2 = add article")
#appSuche.translate("TextKeyF11", "F11 = print location")
#appSuche.translate("TextKeyF12", "F12 = print barcode")

appSuche.addLabel("infoAnzahl",  str(GetStockZahl()) + " " + appSuche.translate("TextArticleInStock", "Article in stock"))
appSuche.bindKey("<Return>", Suche)
appSuche.bindKey("<F1>", StockChange)
appSuche.bindKey("<F2>", StockChange)
appSuche.bindKey("<F4>", BtnStockGraph)
appSuche.bindKey("<F11>", BtnPrintOrt)
appSuche.bindKey("<F12>", BtnPrintBarcode)
appSuche.bindKey("<Delete>", Delete)
appSuche.setStopFunction(SaveIt)

#appSuche.go(BlueLoad("LANG", "DATA/DATA"))
appSuche.go("de")
