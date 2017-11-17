#!/usr/bin/env python3
from libs.appjar0830 import gui  
from BlueFunc import BlueMkDir, BlueLenDatei, BlueLoad, BlueSave
from debug import Debug
import os
import subprocess
from random import randint
import send
import shutil

appMasch = gui("Maschinen", "600x600")

appMasch.setStretch("both")
appMasch.setSticky("nesw")

appMasch.addImage("M1", "Maschinen/Motorsäge/Stihl/MS/150C-E/0.gif", 0, 0)
#appMasch.setSticky("M1")
#appMasch.setImageSize("M1", 100, 100)

DATAFile = "Maschinen/Motorsäge/Stihl/MS/150C-E/DATA"
TeileListe = str(BlueLoad("Index", DATAFile)).split("|")
Debug("TeileListe " + str(TeileListe))

ListeDerTeile = []

for Teil in TeileListe:
	Debug("Teil " + Teil)
	Artikel = BlueLoad("A" + Teil, DATAFile)
	Lieferant = BlueLoad("L" + Teil, DATAFile)

	ID = send.SendeSucheStock(Artikel, "", Lieferant, "")
	ID = ID.split("<K>")[0]
	print("ID " + ID)

	Linie = Teil

	if not ID == "0":
		GetArtInfo = str(send.StockGetArtInfo("(zkz)Name(zkz)Ort(zkz)PreisVK(zkz)Anzahl", ID))
		Name = GetArtInfo.split(" | ")[1]
		Ort = GetArtInfo.split(" | ")[2]
		PreisVK = GetArtInfo.split(" | ")[3]
		Anzahl = GetArtInfo.split(" | ")[4]
		print(GetArtInfo)
		Linie = Teil + " : " + Name + " | " + Ort + " | " + PreisVK + " | " + Anzahl
	ListeDerTeile.append(Linie)

appMasch.addListBox("L1", ListeDerTeile, 0, 1)
appMasch.go()
