#!/usr/bin/env python
import os

if os.path.exists("/home/phablet"):
	DIR = "/home/phablet/.local/share/zk-data.bluekenny/"
else: DIR = ""

def Debug(text):
	file = open(DIR + "DEBUGING", "a")
	print("Debug -> " + str(text))
	file.write("\n" + str(text))
	file.close
