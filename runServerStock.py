#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import platform
import os
while True:
    #os.system("git pull origin master")
    time.sleep(1)
    if platform.system() == "Linux": os.system("python3 ./ServerStock.py")
    if platform.system() == "Windows": os.system("ServerStock.py")
    time.sleep(3)
