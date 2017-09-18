#!/usr/bin/env python3
import sys
import socket
import time
from debug import * 
from BlueFunc import BlueMkDir, BlueLenDatei, BlueLoad, BlueSave
import os
while True:
	os.system("git pull origin master") 
	time.sleep(1)
	os.system("python3 ./Server.py")
	time.sleep(3)
