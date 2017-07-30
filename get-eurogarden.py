#!/usr/bin/env python3
#import convert
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

#for x in os.listdir(DataPreis): os.remove(DataPreis + x)

# http://pyautogui.readthedocs.io/en/latest/cheatsheet.html

Debug(" ")

for file in os.listdir("text/"):
	Debug("Datei " + file)

	DataRechnung = open("text/" + file, "r").read()
	Begin = open(DataPfad + "Begin").read()
	for i in open("text/" + file, "r").readlines():
		#print("This \n" + i.rstrip())
		#print("VS \n" + Begin.rstrip())
		if Begin.rstrip() in i.rstrip(): Begin = i.rstrip()
	Debug("Begin : " + Begin)
	End = open(DataPfad + "End").read()
	Debug("End : " + End)
	DataRechnung = DataRechnung.split(Begin)[1]
	DataRechnung = DataRechnung.split(End)[0]

	for Linie in DataRechnung.split("\n"):
		if not Linie.rstrip() == "": 
			Worte = Linie.split(" ")
		else: Worte = ""
		if len(Worte) > 5:
			Debug(" ")
			Debug("Linie : " + Linie)
			Debug("Worte : " + str(Worte))
			Art = Worte[0].lower()
			Debug("Art : " + Art)
			Filepath = DataPreis + Art
			Debug("Filepath : " + Filepath)
			Anzahl = Worte[-6]
			Debug("Anzahl : " + Anzahl)
			PreisEK = Worte[-2]
			Debug("PreisEK : " + str(PreisEK))
			PreisVKH = Worte[-4]
			Debug("PreisVKH : " + str(PreisVKH))
			PreisVK = RoundUp05(float(PreisVKH) * 1.21)
			Debug("PreisVK : " + str(PreisVK))

			Name = Linie.split(Worte[0] + " ")[1]
			Name = Name.split(" " + Worte[-6] + " " + Worte[-5] + " " + Worte[-4] + " " + Worte[-3] + " " + Worte[-2] + " " + Worte[-1])[0]
			Debug("Name : " + Name)
			BurkardtCode = GetBurkardtCode(title, Art)
			Debug("BurkardtCode : " + BurkardtCode)

			BlueSave("Lieferant", title, Filepath)
			BlueSave("Name", Name, Filepath)
			BlueSave("Anzahl", Anzahl, Filepath)
			BlueSave("PreisVKH", PreisVKH, Filepath)
			BlueSave("PreisVK", PreisVK, Filepath)
			BlueSave("PreisEK", PreisEK, Filepath)
			BlueSave("BurkardtCode", BurkardtCode, Filepath)

	StockIt()
