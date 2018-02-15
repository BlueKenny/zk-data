#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from libs.appjar0830 import gui 
#from numpy import sin, pi, arange
import random
from libs.send import *
import sys
try: import matplotlib
except:
    if platform.system() == "Linux": os.system("pip3 install --user matplotlib")

if len(sys.argv) == 2:
    ID = sys.argv[1]

def Datum_Anzahl(ID):
    local_db.connect()
    query = Bewegung.select().where((Bewegung.bcode == str(str(ID))))
    x = []
    y = []
    for ThisBewegung in query:
        x.append(ThisBewegung.datum)
        y.append(ThisBewegung.end)
    local_db.close()

    def generate(btn):
        # *getXY() will unpack the two return values
        # and pass them as separate parameters
        app.updatePlot("p1", *getXY())
        showLabels()

    def showLabels():
        axes.legend(['Stock von ' + str(ID)])
        axes.set_xlabel("Zeit")
        axes.set_ylabel("Anzahl")
        app.refreshPlot("p1")

    app = gui(handleArgs=False)

    #app.addLabel("ID", "123456")
    axes = app.addPlot("p1", x, y)
    showLabels()
    #app.addButton("Generate", generate)
    app.go()

Datum_Anzahl(ID)
