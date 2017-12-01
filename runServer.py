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
			Debug("Update von " + url.split("/")[-1].rstrip())
			urllib.request.urlretrieve(url, url.split("/")[-1].rstrip())
		Debug("Update Ende")
	time.sleep(1)
	os.system("python3 ./Server.py")
	time.sleep(3)
