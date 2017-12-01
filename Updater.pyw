#!/usr/bin/env python3
from libs.appjar0830 import gui
from BlueFunc import *
from debug import Debug

import urllib.request

MAXURLs = len(open("ListURL", "r").readlines())
CounterURL = 0

print(Date())
def Update():
	global CounterURL
	url = open("ListURL", "r").readlines()[CounterURL]
	Name = url.split("/")[-1].rstrip()
	if not "Server" in Name:
		Datei = url.split("/zk-data/master/")[-1].rstrip()
		if "/" in Datei: BlueMkDir(Datei.replace(Datei.split("/")[-1], ""))
		Debug("Update von " + Name + " (" + Datei + ")")
		appPage.setLabel("Title", "Datei " + Name + " wird aktualisiert")
		urllib.request.urlretrieve(url, Datei)
		if ".py" in Name and os.path.exists("/home"): os.system("chmod +x " + Datei)
	
	CounterURL = CounterURL + 1
	if CounterURL == MAXURLs:
		Debug("Update Ende")
		BlueSave("LastUpdate", Date(), "DATA")
		appPage.stop()
	else:
		appPage.after(500, Update)

appPage = gui("Update ZK-DATA", "300x300")
appPage.addLabel("Title", "...")
appPage.after(500, Update)
Debug("Update Startet")
appPage.go()


