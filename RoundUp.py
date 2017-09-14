#!/usr/bin/env python

# Round UP 0.5
def RoundUp05(Zahl): # 00.00
	Zahl = float(Zahl) * 10.0000
	ZahlRest = Zahl - int(Zahl)
	if ZahlRest < 0.5: ZahlRest = 0.5000
	else: ZahlRest = 1.0000
	Zahl = int(Zahl) + ZahlRest
	Zahl = float(Zahl) / 10.0000
	return Zahl
