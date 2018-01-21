#!/usr/bin/env python3

import pyperclip
from libs.send import *
import subprocess

OldData = ""
	

while True:#def Check():
	NewData = pyperclip.paste()

	if not OldData == NewData:
		print(NewData)
		OldData = NewData
		
		DATA_ID = SendeSucheStock(NewData, "", "").split("<K>")
		if DATA_ID[0] == "0":
			command = subprocess.Popen(["./Popup.pyw", DATA_ID[0], NewData])
		else:
			command = subprocess.Popen(["./Popup.pyw", DATA_ID[0]])
	
		
		

