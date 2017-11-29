#!/usr/bin/env python

DIR = ""
#DIR = "/home/phablet/.local/share/zk-data.bluekenny/"

def Debug(text):
	file = open(DIR + "DEBUGING", "a")
	print("Debug -> " + str(text))
	file.write("\n" + str(text))
	file.close
