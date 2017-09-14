#!/usr/bin/env python

def RoundUp05(Zahl): # 0.00
	Zahl = float(Zahl) * 10.0000
	ZahlRest = Zahl - int(Zahl)
	if ZahlRest < 0.5: ZahlRest = 0.5000
	else: ZahlRest = 1.0000
	Zahl = int(Zahl) + ZahlRest
	Zahl = float(Zahl) / 10.0000
	return Zahl

def RoundUp0005(Zahl): # 0.0000	
	Zahl = float(Zahl) * 10.000000
	ZahlRest = Zahl - int(Zahl)
	if ZahlRest < 0.5: ZahlRest = 0.500000
	else: ZahlRest = 1.000000
	Zahl = int(Zahl) + ZahlRest
	Zahl = float(Zahl) / 10.0000
	return Zahl
