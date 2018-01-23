#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pyperclip
from libs.send import *
import subprocess
import platform
import os

# for autostart on windows
# copy a link in
# C:\users\<your username>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup

OldData = ""

print("os: " + str(platform.system()))	

while True:#def Check():
	NewData = pyperclip.paste()

	if not OldData == NewData and not NewData == "":
		print(NewData)
		OldData = NewData
		
		DATA_ID = SendeSucheStock(NewData, "", "").split("<K>")
		print("DATA_ID " + str(DATA_ID))
		if DATA_ID[0] == "0" or "P" in DATA_ID[0]:
			if platform.system() == "Linux":
				command = subprocess.Popen("./Popup.pyw 0 " + str(NewData), shell=True)
			else:
				command = subprocess.Popen("Popup.pyw 0 " + str(NewData), shell=True)
		else:
			if platform.system() == "Linux":
				command = subprocess.Popen("./Popup.pyw " + str(DATA_ID[0]), shell=True)
			else:
				command = subprocess.Popen("Popup.pyw " + str(DATA_ID[0]), shell=True)
	
		
		

