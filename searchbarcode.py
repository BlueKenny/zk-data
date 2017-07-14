#!/usr/bin/env python
import os

def GetBurkardtCode(lieferant, artikel):
	Pfad = "barcode/" + lieferant + "/" + str(len(artikel)) + "/"
	print(Pfad)
	if os.path.exists(Pfad + str(artikel)):
		print("OK")
		code = open(Pfad + str(artikel), "r").readlines()[0].rstrip()
		print(code)
		return code
	else:
		print("NO")
		return "0"

GetBurkardtCode("eurogarden", "mrcp052033")
