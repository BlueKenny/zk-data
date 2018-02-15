#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

if os.path.exists("/home/phablet"):
	DIR = "/home/phablet/.local/share/zk-data.stock/"
	from BlueFunc import *
else:
	DIR = ""
	from .BlueFunc import *

BlueMkDir(DIR + "DEBUG")


def Debug(text):
	DATE = Date()
	directory = DIR + "DEBUG/"
	for x in sorted(range(2, 4), reverse=True):
		directory = directory  + DATE.split("-")[-x] + "/"
		BlueMkDir(directory)
	file = open(directory + DATE.split("-")[-1] + "-DEBUG", "a")
	print("Debug -> " + str(text))
	file.write("\n" + str(text))
	file.close
