import csv
import sys
import requests
from urllib.error import HTTPError, URLError
from datetime import date
from distro import info
appName="Toulouse'n Feu"

def strZero(int):
    if int < 10:
        return "0"+str(int)
    return str(int)

def readFromTo(filename,list,ignore=0,Filedelimiter=","):
    if ignore > 0:
        deleteRow(filename,ignore)
        filename=filename.replace(".csv","")+"_ignore.csv"
    with open(filename, "r") as file:
        readerObj = csv.DictReader(file, delimiter=Filedelimiter)
        for row in readerObj:
            list.append(dict(row))

def deleteRow(filename,ignore):
    with open(filename, "r") as cin, open(filename.replace(".csv","")+"_ignore.csv", "w+") as cout:
        fileOut = csv.writer(cout)
        for row in csv.reader(cin):
            if(ignore == 0):
                fileOut.writerow(row)
            else:
                ignore-=1

def getNormales(column,month):
    for row in tempNormales:
        if int(row["Month"]) == month:
            return row[column]

def getTodayTemps():
    returnValue = []
    for i in range(0, 22, 3):
        todayDate = (date.today()).strftime("%Y-%m-%d ")+strZero(i)+":00:00"
        for row in infoClimat:
            if row["dh_utc"] == todayDate:
                returnValue.append(row["temperature"])
    return returnValue
                


# query the token id from the text file
try :
    tokenId = open('key.txt').readline()
except OSError:
    print("["+appName+"] : Can't open the file 'key.txt'")
    sys.exit()

# sets up today's date, the URL, and global variables
today = (date.today()).strftime("%Y-%m-%d")
URL = "https://www.infoclimat.fr/opendata/?method=get&format=csv&stations[]=07630&start="+today+"&end="+today+"&token="+tokenId
tempNormales = []
infoClimat = []

# saves the file from https://www.infoclimat.fr/opendata/
try :
    open("export_infoclimat.csv", "wb").write((requests.get(URL)).content)
except HTTPError as e:
    print("["+appName+"] : HTTPError ("+str(e)+")")
    sys.exit()
except URLError as e:
    print("["+appName+"] : URLError ("+str(e)+")")
    sys.exit()
except Exception as e:
    print("["+appName+"] : Unexpected Error ("+str(e)+")")
    sys.exit()
    
# tests if the file is correct
if open('export_infoclimat.csv').readline() != "# METADATA:\n":
    print("["+appName+"] : Wrong token id or ip address")
    sys.exit()

# sets up the lists of temperature for today
readFromTo("normales.csv",tempNormales)
readFromTo("export_infoclimat.csv",infoClimat,4,";")

# print tests
print("Normal Temperature for this month : ",getNormales('Temp',(date.today()).month))
print("Normal Temperature for this month : ",getNormales('MaxTemp',(date.today()).month))
print("Normal Temperature for this month : ",getNormales('MinTemp',(date.today()).month))
print("Today's temperatures : ",getTodayTemps())