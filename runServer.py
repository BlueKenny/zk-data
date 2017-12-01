#!/usr/bin/env python3
import sys
import socket
import time
from debug import * 
from BlueFunc import BlueMkDir, BlueLenDatei, BlueLoad, BlueSave
import os
try: 
	import urllib.request
	MakeUpdate = True
except: MakeUpdate = False
Debug("MakeUpdate : " + str(MakeUpdate))
while True:
	#os.system("git pull origin master") 
	if MakeUpdate:
		Debug("Update Startet")
		for url in open("ListURL", "r").readlines():
			Name = url.split("/")[-1].rstrip()
			Datei = url.split("/zk-data/master/")[-1].rstrip()
			if "/" in Datei:
				DIRS = Datei.replace(Datei.split("/")[-1], "")
				print(DIRS)
				#for DIRS in Datei.split("/"):
				#	if not DIRS == Datei.split("/")[-1]:				
				#		BlueMkDir()
			Debug("Update von " + Name + " (" + Datei + ")")
			urllib.request.urlretrieve(url, Datei)
			if ".py" in Datei and os.path.exists("home"): os.system("chmod +x " + Datei)
		Debug("Update Ende")
	time.sleep(1)
	os.system("python3 ./Server.py")
	time.sleep(3)
