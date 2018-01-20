#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys

from libs.appjar0830 import gui
from libs.RoundUp import *
from libs.debug import Debug
from random import randint
from libs.send import *
from libs.barcode import *
import sys
import csv


from libs.CheckConf import *
string = {}
with codecs.open("LANG/" + BlueLoad("LANG", "DATA/DATA") + ".csv", "r", "utf-8") as csvfile:
	reader = csv.reader(csvfile, delimiter=":", quotechar="\"")
	for eachLine in reader:
		try: string[int(eachLine[0])] = eachLine[1]
		except: True
EntryList=["Barcode", "Artikel", "Lieferant", "Name", "Ort", "PreisEK", "PreisVKH", "PreisVK", "Anzahl"]
EntryList2=[string[4],  string[5], string[6], string[7], string[8], string[0], string[1], string[2], string[9]]

if len(sys.argv) == 1:
	ID = StockSetBCode()
	IDExists = False
else:
	ID = sys.argv[1]
	IDExists = True

def Save():
	print("Save")
	ServerInfo = StockGetArtInfo(EntryList, ID).split(" | ")
	del ServerInfo[0]# Remove ID from List
	#print(ServerInfo)
	#print(StartInfo)
	if not ServerInfo == StartInfo and IDExists and not PID:
		appChange.infoBox(string[33], string[36], parent=None)
	else:
		print("Send Data to Server")
		for Entry in EntryList:
			print("Save " + str(Entry))
			StockSetArtInfo(ID, Entry, appChange.getEntry(EntryList2[EntryList.index(Entry)]))
	return True

def VerifyInput(Entry):
	print("VerifyInput")
	Float = ["PreisEK", "PreisVKH", "PreisVK"]
	Int = ["Barcode", "Anzahl"]
	String = ["Artikel", "Lieferant", "Name", "Ort"]
	ConvertedEntry=EntryList[EntryList2.index(Entry)]
	print("Verify ConvertedEntry " + str(ConvertedEntry))

	if ConvertedEntry == "Ort":
		print("Verify this input " + str(appChange.getEntry(Entry)))
		myLocation = appChange.getEntry(Entry).replace(",", ".").upper()
		appChange.setEntry(Entry, myLocation)

	if ConvertedEntry in Int:
		print("Verify this input " + str(appChange.getEntry(Entry)))
		myInt = appChange.getEntry(Entry)
		appChange.setEntryMaxLength(Entry, 13)
		try:	
			appChange.setEntry(Entry, int(myInt))
		except:
			if ConvertedEntry == "Barcode":	appChange.setEntry(Entry, IDToBarcode(ID))
			else: appChange.setEntry(Entry, "0")
	if ConvertedEntry in Float:
		print("Verify this input " + str(appChange.getEntry(Entry)))
		myFloat = appChange.getEntry(Entry)
		myFloat = myFloat.replace(",", ".")
		try:
			if ConvertedEntry == "PreisEK":
				print("PreisEK")
				myFloat = RoundUp0000(myFloat)
				appChange.setEntry(Entry, float(myFloat))
			if ConvertedEntry == "PreisVKH":
				print("PreisVKH")
				myFloat = RoundUp0000(myFloat)
				appChange.setEntry(EntryList2[EntryList.index("PreisVK")], RoundUp05(myFloat*1.21), callFunction=False)
				myFloat = RoundUp0000(float(appChange.getEntry(EntryList2[EntryList.index("PreisVK")]))/1.21)
				appChange.setEntry(Entry, float(myFloat))
			if ConvertedEntry == "PreisVK":
				print("PreisVK")
				myFloat = RoundUp05(myFloat)
				appChange.setEntry(EntryList2[EntryList.index("PreisVKH")], RoundUp0000(myFloat/1.2100), callFunction=False)
				myFloat = RoundUp05(float(appChange.getEntry(EntryList2[EntryList.index("PreisVKH")]))*1.21)
				appChange.setEntry(Entry, float(myFloat))

			
			
		except:
			appChange.setEntry(Entry, "")
				
			
			
	

def VerifyChanges():
	print("VerifyChanges")
	UserMadeChanges = False
	for Entry in EntryList2:
		NewInfo = appChange.getEntry(Entry)
		OldInfo = StartInfo[EntryList2.index(Entry)]
		if not NewInfo == OldInfo:
			UserMadeChanges = True
	if UserMadeChanges:
		if appChange.yesNoBox(string[33], string[34], parent=None):
			if Save(): return True
			else:
				appChange.infoBox(string[26], string[35], parent=None)
				return False
		else: return True
	else:
		return True

def BtnStockGraph(btn):
	if os.path.exists("/home"):
		COMMAND = "./ArtGraph.py "
	else: COMMAND = "ArtGraph.py "
	os.system(COMMAND + str(ID))

if "P" in ID:
	print("P")
	PID = ID
	ID = StockSetBCode()
else: PID = False

ID = int(ID)
appChange = gui(string[32], "800x600", handleArgs=False) 
appChange.setBg("#ffffff")
appChange.addLabel("Title", str(ID))

StartInfo=[]# App Started with these informations
if not PID:
	print("Exists")
	DATA = StockGetArtInfo(EntryList, ID).split(" | ")
else:
	print("New")
	DATA = StockGetArtInfo(EntryList, PID).split(" | ")
	DATA.insert(1, IDToBarcode(ID))
	DATA.insert(5, "")
	DATA.insert(9, 0)
	DATA[0] = ID
print("DATA " + str(DATA))
print("EntryList2 " + str(EntryList2))
for Entry in EntryList2:
	print("Entry " + str(Entry))
	appChange.addLabelEntry(Entry)
	appChange.setEntryChangeFunction(Entry, VerifyInput)
	if IDExists:
		appChange.setEntry(Entry, DATA[EntryList2.index(Entry) + 1], callFunction=False)
		StartInfo.append(DATA[EntryList2.index(Entry) + 1])
	else:
		appChange.setEntry(Entry, "", callFunction=False)
		StartInfo.append("")

appChange.setStopFunction(VerifyChanges)
appChange.bindKey("<F4>", BtnStockGraph)
appChange.go()

