#!/usr/bin/env python3
import convert
from BlueVar import *
import os
import sys
from debug import *
from RoundUp import *
from searchbarcode import *
from Stock import *

title = "eurogarden"

DataFile = title + "Data"
DataPfad = title + "-data/"
DataPreis = title + "-preis/"

if not os.path.exists(DataPfad): os.mkdir(DataPfad)
if not os.path.exists(DataPreis): os.mkdir(DataPreis)

for x in os.listdir(DataPreis): os.remove(DataPreis + x)

# http://pyautogui.readthedocs.io/en/latest/cheatsheet.html

Debug(" ")

for file in os.listdir("text/"):
	Debug("Datei " + file)

	DataRechnung = open("text/" + file, "r").read()
	Begin = open(DataPfad + "Begin").read()
	Debug("Begin : " + Begin)
	#End = open(DataPfad + "End").read()
	#Debug("End : " + End)
	DataRechnung = DataRechnung.split(Begin)[1]
	#DataRechnung = DataRechnung.split(End)[0]

	for Linie in DataRechnung.split("\n"):
		if not Linie.rstrip() == "":
			Worte = Linie.split(" ")
			print(Worte)
		

			Debug(" ")
			Debug("Linie : " + Linie)
			Art = Worte[0].lower()
			Debug("Art : " + Art)
			Filepath = DataPreis + Art
			Debug("Filepath : " + Filepath)
			Anzahl = Worte[len(Worte)-5]
			Debug("Anzahl : " + Anzahl)
			PreisVKH = Worte[len(Worte)-3]
			PreisVKH = PreisVKH.replace(",", ".")
			PreisVKH = float(PreisVKH) / 100.0000
			Debug("PreisVKH : " + str(PreisVKH))

			Name = Linie.split(Worte[0] + " ")[1]
			Name = Name.split(" " + Worte[-5] + " " + Worte[-4] + " " + Worte[-3] + " " + Worte[-2] + " " + Worte[-1])[0]
			Debug("Name : " + Name)
			BurkardtCode = GetBurkardtCode(title, Art)
			Debug("BurkardtCode : " + BurkardtCode)
			
			PreisVK = float(PreisVKH) * 1.2100
			PreisVK = RoundUp05(PreisVK)
			Debug("PreisVK : " + str(PreisVK))
			PreisEK = Worte[len(Worte)-1]
			Debug("PreisEK : " + str(PreisEK))


			BlueSave("Name", Name, Filepath)
			BlueSave("Anzahl", Anzahl, Filepath)
			BlueSave("PreisVKH", PreisVKH, Filepath)
			BlueSave("PreisVK", PreisVK, Filepath)
			BlueSave("PreisEK", PreisEK, Filepath)
			BlueSave("BurkardtCode", BurkardtCode, Filepath)

	StockIt()
