#!/usr/bin/env python
import os

def BlueLen(File):
	if os.path.exists(File): 
		Datei = open(File, "r")
		DateiDatenIndex = Datei.readlines()
		Datei.close()
		return len(DateiDatenIndex)

def BlueMkDir(directory):
	if not os.path.exists(directory):
		os.mkdir(directory)
