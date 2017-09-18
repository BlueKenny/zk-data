#!/usr/bin/env python3
import sys
import socket
import time
from debug import * 
import os

os.system("git pull origin master") 
time.sleep(1)
os.system("python3 ./Server.py &")
time.sleep(2)
os.system("python3 ./SucheStock.pyw")
