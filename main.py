#!/usr/bin/env python3
#!/usr/bin/env python2
from datetime import date

from src.toulousenfeu import Toulousenfeu
from src.readfile import *
from src.connect import App

# App initialisation
app = App("Toulouse'n Feu")
app.setToken()
app.setURL()
app.connect()

# Main
tlf = Toulousenfeu(readFile("data/normales.csv"),readFile("data/export_infoclimat.csv",4,";"))
print("Normale Minimum :",tlf.moyNormale(date.today(),tlf.monthsNormalesMin))
print("Normale Maximum :",tlf.moyNormale(date.today(),tlf.monthsNormalesMax))
print("Minimum Aujourd'hui :",tlf.findMin())
print("Maximum Aujourd'hui :",tlf.findMax())