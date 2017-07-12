#!/usr/bin/env python
import os
from debug import *

if not os.path.exists("text/"): os.mkdir("text/")
if not os.path.exists("png/"): os.mkdir("png/")

Debug("\n\n\n\n\n\n")
Debug("Start")

Debug("Ordner werden bereinigt")
#for x in os.listdir("png/"): os.remove("png/" + x)
for x in os.listdir("text/"): os.remove("text/" + x)

if os.path.exists("/etc/"): tesseract = "tesseract"
else: tesseract = "tesseract.exe"
Debug("Var tesseract : " + tesseract)

for PNG in os.listdir("png/"):
	if not PNG == "Thumbs.db":
		Debug("Convertiere " + PNG + " zu TEXT")
		os.system(tesseract + " png/" + PNG + " text/" + PNG)
