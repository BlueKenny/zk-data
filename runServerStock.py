#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import platform
import os
while True:
    #os.system("git pull origin master")
    time.sleep(1)
    if platform.system() == "Linux": os.system("python3 ./Server.py")
    if platform.system() == "Windows": os.system("Server.py")
    time.sleep(3)
