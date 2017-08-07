#!/usr/bin/env python
import os
import codecs
SplitIt = "&zKz&"

def BlueLoad(VarName, File):
	if os.path.exists(File): 
		Datei = codecs.open(File, "r", encoding="utf-8")
		DateiDatenIndex = Datei.readlines()
		Datei.close()
		Gefunden=False
		for AlleLinien in DateiDatenIndex:
			LinienVarName = AlleLinien.split(SplitIt)[0]
			if VarName == LinienVarName:	
				SavedData = AlleLinien.split(SplitIt)[1].rstrip()
				return SavedData

def BlueSave(VarName, VarData, File):
	if os.path.exists(File): 
		Datei = codecs.open(File, "r", encoding="utf-8")
		DateiDatenIndex = Datei.readlines()
		Datei.close()
		Gefunden=False
		for AlleLinien in DateiDatenIndex:
			LinienVarName = AlleLinien.split(SplitIt)[0]
			if VarName == LinienVarName:	
				Gefunden=True
				LinienVarData = AlleLinien.split(SplitIt)[1]

				Datei = codecs.open(File, "r", encoding="utf-8")
				DateiDaten = Datei.read()
				Datei.close()

				Datei = codecs.open(File, "w", encoding="utf-8")
				Datei.write(DateiDaten.replace(str(LinienVarName) + str(SplitIt) + str(LinienVarData), str(VarName) + str(SplitIt) + str(VarData) + "\n"))
				Datei.close()
		if not Gefunden:
			Datei = open(File, "a")
			Datei.write("\n" + str(VarName) + str(SplitIt) + str(VarData))
			Datei.close()
	else:
		Datei = open(File, "w")
		Datei.write(str(VarName) + str(SplitIt) + str(VarData))

