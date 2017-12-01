#!/usr/bin/env python3
from libs.appjar0830 import gui
from BlueFunc import *
from debug import Debug

try: 
	import urllib.request
	MakeUpdate = True
except: MakeUpdate = False

if MakeUpdate:
		Debug("Update Startet")
		for url in open("ListURL", "r").readlines():
			Name = url.split("/")[-1].rstrip()
			if not "Server" in Name:
				Datei = url.split("/zk-data/master/")[-1].rstrip()
				if "/" in Datei: BlueMkDir(Datei.replace(Datei.split("/")[-1], ""))
				Debug("Update von " + Name + " (" + Datei + ")")
				urllib.request.urlretrieve(url, Datei)
				if ".py" in Datei and os.path.exists("home"): os.system("chmod +x " + Datei)
		Debug("Update Ende")
