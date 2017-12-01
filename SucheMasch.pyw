#!/usr/bin/env python3
from libs.appjar0830 import gui  
from BlueFunc import *
from debug import Debug
import os
import subprocess
from random import randint
import send
import shutil
DIREXPLO = "Maschinen/"
DIRMASCH = "Maschinen/"
DATAFile = "Maschinen/"
IndexListe = []
ListeDerTeile = [] # DATA
CurrentTeilPos = 0


if not Date() == BlueLoad("LastUpdate", "DATA"):
	try: os.system("./Updater.pyw")
	except: os.system("Updater.pyw")

def SelectExplo(btn):
	global DIREXPLO; global DIRMASCH
	global DATAFile; global IndexListe; global ListeDerTeile
	global CurrentTeilPos
	print("SelectMasch")
	DIREXPLO = appMasch.openBox(title="Maschine wählen", dirName=DIRMASCH, fileTypes=[("images", "*.gif")], asFile=False, parent=None)
	if ".gif" in DIREXPLO:
		DIRMASCH = DIREXPLO[:-len(DIREXPLO.split("/")[-1])]
		appMasch.setStatusbar(DIRMASCH.split("Maschinen")[1][:-1] + "    :    " + DIREXPLO.split("/")[-1].replace(".gif", ""), field=0)
	appMasch.setImage("Image", DIREXPLO)
	Debug("DIREXPLO " + DIREXPLO)
	
	DATAFile = DIREXPLO.replace(".gif", "-DATA")
	IndexListe = str(BlueLoad("Index", DATAFile)).split("|")
	Debug("IndexListe " + str(IndexListe))

	appMasch.clearListBox("L1", callFunction=True)
	del ListeDerTeile[:]
	for x in IndexListe:
		try: ListeDerTeile.append(BlueLoad("Last" + x, DATAFile))
		except: ListeDerTeile.append(x)
	appMasch.updateListBox("L1", ListeDerTeile, select=False)

	CurrentTeilPos = randint(0, len(IndexListe))

	appMasch.registerEvent(Check)


appMasch = gui("Maschinen", "600x600")
#appMasch.setGeometry("Fullscreen")

appMasch.setStretch("both")
appMasch.setSticky("nesw")

appMasch.addToolbar(["Maschine wählen"], SelectExplo, findIcon=True)
appMasch.addStatusbar(header="", fields=1)

appMasch.addImage("Image", "Burkardt.gif", 1, 0)




def Check():
	global DIREXPLO
	global CurrentTeilPos
	print("Check")
	
	Debug("CurrentTeilPos " + str(CurrentTeilPos))
	Teil = IndexListe[CurrentTeilPos]
	Debug("Teil " + str(Teil))
	Artikel = BlueLoad("A" + Teil, DATAFile)
	Lieferant = BlueLoad("L" + Teil, DATAFile)

	if ListeDerTeile[CurrentTeilPos] == None: ListeDerTeile[CurrentTeilPos] = ""
	if len(ListeDerTeile[CurrentTeilPos].split(":")) == 3:
		ID = ListeDerTeile[CurrentTeilPos].split(":")[1].replace("[", "").replace("]", "")
	else:
		ID = send.SendeSucheStock(Artikel, "", Lieferant)
		ID = ID.split("<K>")[0]
	print("ID " + ID)

	Linie = Teil
	
	if not ID == "0":
		GetArtInfo = str(send.StockGetArtInfo("(zkz)Name(zkz)Ort(zkz)PreisVK", ID))
		Name = GetArtInfo.split(" | ")[1]
		Ort = GetArtInfo.split(" | ")[2]
		PreisVK = GetArtInfo.split(" | ")[3]
		Anzahl = GetArtInfo.split(" | ")[4]
		print(GetArtInfo)
		Linie = Teil + " : [" + ID + "] : " + Name + " | " + Ort + " | " + PreisVK + " | " + Anzahl
	else:
		Linie = Teil + " : " + str(Artikel) + " ( " + str(Lieferant) + " )"
	ListeDerTeile[CurrentTeilPos] = Linie
	BlueSave("Last" + Teil, Linie, DATAFile)
	

	appMasch.updateListBox("L1", ListeDerTeile, select=False)

	Debug("len(IndexListe) " + str(len(IndexListe)))
	if len(IndexListe) - 1 == CurrentTeilPos: CurrentTeilPos = 0
	else: CurrentTeilPos = CurrentTeilPos + 1


appMasch.setPollTime(2000)
appMasch.addListBox("L1", ListeDerTeile, 1, 1)
appMasch.go()
