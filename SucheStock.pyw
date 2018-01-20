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
string = {}
with codecs.open("LANG/" + BlueLoad("LANG", "DATA/DATA") + ".csv", "r", "utf-8") as csvfile:
	reader = csv.reader(csvfile, delimiter=":", quotechar="\"")
	for eachLine in reader:
		try: string[int(eachLine[0])] = eachLine[1]
		except: True

EntryList=["Barcode", "Artikel", "Lieferant", "Name", "Ort", "PreisEK", "PreisVKH", "PreisVK", "Anzahl"]
EntryList2=[string[4],  string[5], string[6], string[7], string[8], string[0], string[1], string[2], string[9]]
appSuche = gui(string[12], "800x600") 
appSuche.setBg("#ffffff")

IDToChange = 0

appSuche.addMeter("status"); appSuche.setMeterFill("status", "blue")
appSuche.setMeter("status", 100, text="")


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
	PrintBarcode("", GetData[0], GetData[1], GetData[2], GetData[3])

def BtnPrintOrt(btn):
	PrintLocation(StockGetArtInfo("(zkz)Ort", appSuche.getListItems("Suche")[0].split(" | ")[0]).split(" | ")[1])

def tbFunc(btn):
	global IDToChange
	global appChange
	Debug("btn : " + btn)

	if btn == string[10]:# NEU
		if os.path.exists("/home"):
			COMMAND = "./ChangeStock.pyw"
		else: COMMAND = "ChangeStock.pyw"
		os.system(COMMAND)
		Suche("")
		
	if btn == string[11]:# ÄNDERN
		ID = appSuche.getListBox("Suche")[0].split(" | ")[0]
		if os.path.exists("/home"):
			COMMAND = "./ChangeStock.pyw"
		else: COMMAND = "ChangeStock.pyw"
		os.system(COMMAND + " " + ID)
		#Suche("")

tools = [string[10], string[11]]
appSuche.addToolbar(tools, tbFunc, findIcon=True)

appSuche.addTickOptionBox(string[13], EntryList2)
try:
	for eachAnzeigenOption in BlueLoad("Anzeigen-Stock", "DATA/DATA").split("/"):
		appSuche.setOptionBox(string[13], eachAnzeigenOption, value=True, callFunction=True)
except: print("Anzeigen nicht gefunden")

appSuche.addLabelEntry(string[37])
appSuche.addLabelEntry(string[8])
appSuche.addLabelEntry(string[6])
appSuche.addListBox("Suche")

def Delete(btn):
	Debug("Delete")
	appSuche.setEntry(string[37], "")
	appSuche.setEntry(string[8], "")
	appSuche.setEntry(string[6], "")

def Suche(btn):
	Debug("Suche")
	appSuche.setMeter("status", 0, text=string[27])
	
	AntwortList=SendeSucheStock(appSuche.getEntry(string[37]).replace(" ", ""), appSuche.getEntry(string[8]).upper(), appSuche.getEntry(string[6]).lower())


	appSuche.setMeter("status", 10, text=string[28])
	appSuche.clearListBox("Suche")

	if btn == "first":
		AntwortList = AntwortList.split("<K>")[0]
		Schritt = (100-10)/(1); print(string[29].replace("X", str(Schritt)))
	else:
		Schritt = (100-10)/(len(AntwortList.split("<K>"))-1); print(string[29].replace("X", str(Schritt)))

	for IDs in AntwortList.split("<K>"):
		Debug("Get Info for ID " + str(IDs))
		if not IDs == "" and not IDs == "0"and not IDs == None and not IDs == "None":
			appSuche.setMeter("status", appSuche.getMeter("status")[0]*100 + Schritt, text=string[30])
			print(string[31].replace("X", str(appSuche.getMeter("status")[0] + Schritt)))
			Linie = str(IDs).rstrip()
			SaveIt() # Save All to DATA
			GetThis2 = BlueLoad("Anzeigen-Stock", "DATA/DATA").split("/")
			GetThis = []
			for each in GetThis2:
				GetThis.append(EntryList[EntryList2.index(each)])
				print(GetThis)
			Linie = StockGetArtInfo(GetThis, IDs)

			appSuche.addListItem("Suche", Linie)
			if "P" in IDs:
				appSuche.setListItemBg("Suche", Linie, "#FFF68F")
			else:
				appSuche.setListItemBg("Suche", Linie, "#ffffff")
	appSuche.selectListItemAtPos("Suche", 0, callFunction=False)
	appSuche.setLabel("infoAnzahl", string[20].replace("X",str(GetStockZahl())))
	appSuche.setMeter("status", 100, text="")

def SaveIt():
	Debug("SaveIt")
	for each in EntryList2:
		if appSuche.getOptionBox(string[13])[each]:
			try: AnzeigenListe = AnzeigenListe + "/" + each
			except: AnzeigenListe = each
	try:
		print(AnzeigenListe)
		BlueSave("Anzeigen-Stock", AnzeigenListe, "DATA/DATA")
	except:
		print(string[32])
		BlueSave("Anzeigen-Stock", string[6] + "/" + string[7] + "/" + string[8] + "/" + string[2] + "/" + string[9], "DATA/DATA")
	return True

def StockChange(btn):
	Debug("StockChange")
	IDToChange = appSuche.getListItems("Suche")[0].split(" | ")[0].rstrip()
	Name = "[ " + StockGetArtInfo(["Name"], str(IDToChange)) + " ]"
	if btn == "<F1>": # MINUS
		Anzahl = appSuche.numberBox(string[9], Name + "\n\n" + string[21])
		try:
			SendeChangeAnzahl(IDToChange, "-" + str(int(Anzahl)))
			Debug(IDToChange)
			appSuche.infoBox(string[23], string[24].replace("X", str(int(Anzahl))).replace("N", str(Name)))
			appSuche.setEntry(string[37], IDToChange)
			Suche("first")
		except: appSuche.infoBox(string[26], string[26])
	if btn == "<F2>": # PLUS
		Anzahl = appSuche.numberBox(string[9], Name + "\n\n" + string[22])
		try:
			SendeChangeAnzahl(IDToChange, int(Anzahl))
			Debug(IDToChange)
			appSuche.infoBox(string[23], string[25].replace("X", str(int(Anzahl))).replace("N", str(Name)))
			appSuche.setEntry(string[37], IDToChange)
			Suche("first")
		except: appSuche.infoBox(string[26], string[26])

appSuche.setFocus(string[37])
appSuche.addLabel("info", string[14] + "\n" + string[15] + "\n\n" + string[16] + "\n" + string[17] + "\n" + string[18] + "\n" + string[19])
#appSuche.setListBoxChangeFunction("Suche", tbFunc(string[11]))
appSuche.addLabel("infoAnzahl", string[20].replace("X", str(GetStockZahl())))
appSuche.bindKey("<Return>", Suche)
appSuche.bindKey("<F1>", StockChange)
appSuche.bindKey("<F2>", StockChange)
appSuche.bindKey("<F4>", BtnStockGraph)
appSuche.bindKey("<F11>", BtnPrintOrt)
appSuche.bindKey("<F12>", BtnPrintBarcode)
appSuche.bindKey("<Delete>", Delete)
appSuche.setStopFunction(SaveIt)
appSuche.go()
