#!/usr/bin/env python

def Debug(text):
	file = open("DEBUGING", "a")
	print("Debug -> " + str(text))
	file.write("\n" + str(text))
	file.close
