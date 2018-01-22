#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from .BlueFunc import *

BlueMkDir("DEBUG")


def Debug(text):
	DATE = Date()
	DIR = "DEBUG/"
	for x in sorted(range(2, 4), reverse=True):
		DIR = DIR  + DATE.split("-")[-x] + "/"
		BlueMkDir(DIR)
	file = open(DIR + DATE[-1] + "-DEBUG", "a")
	print("Debug -> " + str(text))
	file.write("\n" + str(text))
	file.close
