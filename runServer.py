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
		urllib.request.urlretrieve("https://raw.githubusercontent.com/BlueKenny/zk-data/master/runServer.py", "runServer.py")
	time.sleep(1)
	os.system("python3 ./Server.py")
	time.sleep(3)
