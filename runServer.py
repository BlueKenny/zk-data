#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import socket
import time
from libs.debug import * 
from libs.BlueFunc import BlueMkDir, BlueLenDatei, BlueLoad, BlueSave
import os
while True:
	#os.system("git pull origin master") 
	time.sleep(1)
	if os.path.exists("/home/"): os.system("python3 ./Server.py")
	else: os.system("Server.py")
	time.sleep(3)
