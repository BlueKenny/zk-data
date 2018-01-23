#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pyperclip
from libs.send import *
import subprocess
import os

# for autostart on windows
# copy a link in
# C:\users\<your username>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup

OldData = ""
	

while True:#def Check():
	NewData = pyperclip.paste()

	if not OldData == NewData:
		print(NewData)
		OldData = NewData
		
		DATA_ID = SendeSucheStock(NewData, "", "").split("<K>")
		if DATA_ID[0] == "0" or "P" in DATA_ID[0]:
			try: command = subprocess.Popen(["./Popup.pyw", "0", str(NewData)], shell=True)
			except: subprocess.Popen("Popup.pyw 0 " + str(NewData), shell=True)
		else:
			try: command = subprocess.Popen(["./Popup.pyw", str(DATA_ID[0])], shell=True)
			except: subprocess.Popen("Popup.pyw " + str(DATA_ID[0]), shell=True)
	
		
		

