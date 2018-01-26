#!/usr/bin/env python3
import os
import platform
import time
import datetime
import subprocess

StopCounter = 6

while True:
	
	time.sleep(10)

	Zeit = str(datetime.datetime.now().time()).split(":")
	Stunden = int(Zeit[0])
	Minuten = int(Zeit[1])

	print("Zeit " + str(Stunden) + ":" + str(Minuten))

	RestZeit = StopCounter * 10
	print("RestZeit " + str(RestZeit))

	if Stunden > 18 and Minuten > 0:
		print("Warnung")
		if platform.system() == "Linux": subprocess.Popen("./Popup.pyw PowerOff " + str(RestZeit), shell=True)
		if platform.system() == "Windows": subprocess.Popen("Popup.pyw PowerOff " + str(RestZeit), shell=True)

		if StopCounter == 0:
			print("AUS")
			if platform.system() == "Linux": os.system("systemctl poweroff")
			if platform.system() == "Windows": os.system("shutdown -s")
			break
		StopCounter = StopCounter - 1
	




