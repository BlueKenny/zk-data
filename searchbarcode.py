#!/usr/bin/env python
import os

def GetBurkardtCode(lieferant, artikel):
	Pfad = "barcode/" + lieferant + "/" + artikel[-3] + artikel[-2] + artikel[-1] + "/"
	print(Pfad)
	if os.path.exists(Pfad + str(artikel)):
		print("OK")
		code = open(Pfad + str(artikel), "r").readlines()[0].rstrip()
		print(code)
		return code
	else:
		print("NO")
		return "0"

