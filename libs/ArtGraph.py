#!/usr/bin/env python3
from libs.appjar0830 import gui 
from numpy import sin, pi, arange
import random
from libs.send import *
import sys

def Datum_Anzahl(ID):

	DATA=StockGetBewegung(ID)
	DATA=DATA.replace("\']", "").replace("[\'", "")
	DATA=DATA.split("\', \'")
	print(DATA)
	x=[]
	y=[]
	for vars in DATA:
		x.append(vars.split("|")[0])
		y.append(vars.split("|")[1])

	def generate(btn):
	    # *getXY() will unpack the two return values
	    # and pass them as separate parameters
	    app.updatePlot("p1", *getXY())
	    showLabels()

	def showLabels():
	    axes.legend(['Stock von ' + str(ID)])
	    axes.set_xlabel("Monate")
	    axes.set_ylabel("Anzahl")
	    app.refreshPlot("p1")

	app = gui()
	#app.addLabel("ID", "123456")
	axes = app.addPlot("p1", x, y)
	showLabels()
	#app.addButton("Generate", generate)
	app.go()
