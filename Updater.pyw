#!/usr/bin/env python3
from libs.appjar0830 import gui
from BlueFunc import *
from debug import Debug
import os
import urllib.request

MAXURLs = len(open("ListURLClient", "r").readlines())
CounterURL = 0

print(Date())
def Update():
	global CounterURL
	url = open("ListURLClient", "r").readlines()[CounterURL]
	Name = url.split("/")[-1].rstrip()

	Datei = url.split("/zk-data/master/")[-1].rstrip()
	if "/" in Datei: BlueMkDir(Datei.replace(Datei.split("/")[-1], ""))
	Debug("Update von " + Name + " (" + Datei + ")")
	appPage.setLabel("Title", "Datei " + Name + " wird aktualisiert")
	try: 
		urllib.request.urlretrieve(url, Datei + ".new")
		os.remove(Datei)
		os.rename(Datei + ".new", Datei)
	except: Debug("Error bei Update : " + url)
	
	CounterURL = CounterURL + 1
	if CounterURL == MAXURLs:
		Debug("Update Ende")
		BlueSave("LastUpdate", Date(), "DATA")
		appPage.stop()
	else:
		appPage.after(500, Update)

appPage = gui("Update ZK-DATA", "400x100")
appPage.addLabel("Title", "...")
appPage.after(500, Update)
Debug("Update Startet")
appPage.go()


