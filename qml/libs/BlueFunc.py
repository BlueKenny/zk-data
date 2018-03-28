#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time
import datetime
import codecs


def BlueMkDir(directory):#	Macht ein verzeichnis wenn es noch nicht existiert
    directory = forPhone(directory)

    if not os.path.exists(directory):
        os.makedirs(directory)
        #os.mkdir(directory)
        
def forPhone(file):
    if os.path.exists("/home/phablet"):
        if not os.path.exists("/home/phablet/.local/zk-data.bluekenny"): os.makedirs("/home/phablet/.local/zk-data.bluekenny")
        if not "/home/phablet/.local/zk-data.bluekenny/" in file:
            file = "/home/phablet/.local/zk-data.bluekenny/" + file
            file = file.replace("//", "/")
    return str(file)

def Date():
    now = datetime.datetime.now()
    zeit = str(now.strftime("%Y-%m-%d"))
    return zeit

def Timestamp():
    return time.time()

def BlueLenDatei(File):	#	Gibt die anzahl linie zuruck in einem dokument
    File = forPhone(File)

    if os.path.exists(File): 
        Datei = open(File, "r")
        DateiDatenIndex = Datei.readlines()
        Datei.close()
        return len(DateiDatenIndex)





SplitIt = "&zKz&"
def BlueLoad(VarName, File):
    File = forPhone(File)

    if os.path.exists(File): 
        try:
            Datei = codecs.open(File, "r", "utf-8")
            DateiDatenIndex = Datei.readlines()
            Datei.close()
        except:
            Datei = codecs.open(File, "r", "latin-1")
            DateiDatenIndex = Datei.readlines()
            Datei.close()
        Gefunden=False
        for AlleLinien in DateiDatenIndex:
            LinienVarName = AlleLinien.split(SplitIt)[0]
            if VarName == LinienVarName:	
                SavedData = AlleLinien.split(SplitIt)[1].rstrip()
                return SavedData

def BlueSave(VarName, VarData, File):
    File = forPhone(File)

    if os.path.exists(File): 
        Datei = open(File, "r", errors="ignore")
        DateiDatenIndex = Datei.readlines()
        Datei.close()
        Gefunden=False
        for AlleLinien in DateiDatenIndex:
            LinienVarName = AlleLinien.split(SplitIt)[0]
            if VarName == LinienVarName:	
                Gefunden=True
                LinienVarData = AlleLinien.split(SplitIt)[1]

                Datei = open(File, "r", errors="ignore")
                DateiDaten = Datei.read()
                Datei.close()

                Datei = open(File, "w")
                Datei.write(DateiDaten.replace(str(LinienVarName) + str(SplitIt) + str(LinienVarData), str(VarName) + str(SplitIt) + str(VarData) + "\n"))
                Datei.close()
        if not Gefunden:
            Datei = open(File, "a")
            Datei.write("\n" + str(VarName) + str(SplitIt) + str(VarData))
            Datei.close()
    else:
        Datei = open(File, "w")
        Datei.write(str(VarName) + str(SplitIt) + str(VarData))

