#!/usr/bin/env python3
from libs.appjar0830 import gui  
from BlueFunc import BlueMkDir, BlueLenDatei, BlueLoad, BlueSave

DIREXPLO = "Maschinen/"
DIRMASCH = "Maschinen/"

appMasch = gui("Maschinen", "600x600")

def save(btn):
	print("save")
	Datei = DIREXPLO.replace(".gif", "-DATA")
	try: Index = BlueLoad("Index", Datei).split("|")
	except: Index = ""

	if not Index == "" and not appMasch.getEntry("Index") in Index:
		Index.append(appMasch.getEntry("Index"))
		SaveThis = ""
		for e in Index:
			if SaveThis == "": SaveThis = e
			else: SaveThis = SaveThis + "|" + e
		BlueSave("Index", SaveThis, Datei)
		
	if Index == "" and not appMasch.getEntry("Index") in Index:
		SaveThis = appMasch.getEntry("Index")
		BlueSave("Index", SaveThis, Datei)
		

	BlueSave("A" + appMasch.getEntry("Index"), appMasch.getEntry("Artikel"), Datei)
	BlueSave("L" + appMasch.getEntry("Index"), appMasch.getEntry("Lieferant"), Datei)

	appMasch.setEntry("Index", int(appMasch.getEntry("Index")) + 1)
	appMasch.setEntry("Artikel", "")

def Maschinen(btn):
	global DIREXPLO; global DIRMASCH
	DIREXPLO = appMasch.openBox(title="Maschine wählen", dirName=DIRMASCH, fileTypes=[("images", "*.gif")], asFile=False, parent=None)
	if ".gif" in DIREXPLO:
		DIRMASCH = DIREXPLO[:-len(DIREXPLO.split("/")[-1])]
		appMasch.setStatusbar(DIRMASCH.split("Maschinen")[1][:-1] + "    :    " + DIREXPLO.split("/")[-1].replace(".gif", ""), field=0)
		appMasch.setButton("Maschine", DIREXPLO.replace(".gif", "").split("Maschinen")[1])


appMasch.addNamedButton("Maschine wählen...", "Maschine", Maschinen)

appMasch.addLabelEntry("Index"); appMasch.setEntry("Index", "1")
appMasch.addLabelEntry("Artikel")
appMasch.addLabelEntry("Lieferant")
appMasch.addButton("Speichern", save)
appMasch.bindKey("<Return>", save)
appMasch.go()
