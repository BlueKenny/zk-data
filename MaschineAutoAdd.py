#!/usr/bin/env python3
from libs.appjar0830 import gui  
from BlueFunc import BlueMkDir, BlueLoad, BlueSave

DIREXPLO = "Maschinen/"
DIRMASCH = "Maschinen/"

appMasch = gui("Maschinen", "600x600")

def save(btn):
	print("save")
	DateiDATA = DIREXPLO.replace(".gif", "-DATA")
	DateiText = DIREXPLO.replace(".gif", ".txt")
	
	
	Index = ""
	for linie in open(DateiText, "r").readlines():
		linie = linie.replace("	", "")
		linie = linie.rstrip()
		platz = linie.split(" ")[0].rstrip()
		print(platz)
		artikel = linie.split(" ")[1].rstrip()
		print(artikel)

		try: Index = BlueLoad("Index", DateiDATA).split("|")
		except: Index = ""

		if not Index == "" and not str(platz) in Index:
			Index.append(str(platz))
			SaveThis = ""
			for e in Index:
				if SaveThis == "": SaveThis = e
				else: SaveThis = SaveThis + "|" + e
			BlueSave("Index", SaveThis, DateiDATA)
		
		if Index == "" and not str(platz) in Index:
			SaveThis = str(platz)
			BlueSave("Index", SaveThis, DateiDATA)
		

		BlueSave("A" + str(platz), str(artikel), DateiDATA)
		BlueSave("L" + str(platz), appMasch.getEntry("Lieferant"), DateiDATA)

def Maschinen(btn):
	global DIREXPLO; global DIRMASCH
	DIREXPLO = appMasch.openBox(title="Maschine wählen", dirName=DIRMASCH, fileTypes=[("images", "*.gif")], asFile=False, parent=None)
	if ".gif" in DIREXPLO:
		DIRMASCH = DIREXPLO[:-len(DIREXPLO.split("/")[-1])]
		appMasch.setStatusbar(DIRMASCH.split("Maschinen")[1][:-1] + "    :    " + DIREXPLO.split("/")[-1].replace(".gif", ""), field=0)
		appMasch.setButton("Maschine", DIREXPLO.replace(".gif", "").split("Maschinen")[1])


appMasch.addNamedButton("Maschine wählen...", "Maschine", Maschinen)

appMasch.addLabelEntry("Lieferant")
appMasch.addButton("Automatisch Speichern", save)
appMasch.bindKey("<Return>", save)
appMasch.go()
