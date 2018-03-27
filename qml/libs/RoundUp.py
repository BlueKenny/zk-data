#!/usr/bin/env python
# -*- coding: utf-8 -*-

def RoundUp05(Zahl): # 0.05
	Zahl = float(Zahl)
	#print("Zahl " + str(Zahl))
	Zahl = int(Zahl*100)/100
	#print("Zahl " + str(Zahl))
	Zahl = float(Zahl) * 10.0000
	#print("Zahl " + str(Zahl))
	ZahlRest = Zahl - int(Zahl)
	#print("ZahlRest " + str(ZahlRest))
	if ZahlRest < 0.5:
		if not ZahlRest == 0:
			ZahlRest = 0.5000
	if ZahlRest > 0.5:  ZahlRest = 1.0000
	#print("ZahlRest " + str(ZahlRest))
	Zahl = int(Zahl) + ZahlRest
	Zahl = float(Zahl) / 10.0000
	return Zahl
def RoundUp0000(Zahl): # 0.0000
	Zahl = float(Zahl) * 10000.0000
	Zahl = int(Zahl)
	Zahl = float(Zahl) / 10000.0000
	return Zahl
def RoundUp00(Zahl): # 0.00
	Zahl = float(Zahl) * 100.0000
	Zahl = int(Zahl)
	Zahl = float(Zahl) / 100.0000
	return Zahl
