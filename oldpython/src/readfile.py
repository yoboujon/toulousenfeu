import csv
import sys
from datetime import datetime

def readFile(filename,ignore=0,Filedelimiter=","):
    """Read a CSV file and returns its content in the list

    :param filename: File name
    :type filename: string
    :param ignore: raws to ignore in the file, defaults to 0
    :type ignore: int, optional
    :param Filedelimiter: Delimits the csv's columns, defaults to ","
    :type Filedelimiter: str, optional
    :return: list read from the csv
    :rtype: list
    """
    list = []
    if ignore > 0:
        deleteRow(filename,ignore)
        filename=filename.replace(".csv","")+"_ignore.csv"
    with open(filename, "r") as file:
        readerObj = csv.DictReader(file, delimiter=Filedelimiter)
        for row in readerObj:
            list.append(dict(row))
    return list

def deleteRow(filename,ignore):
    """Creates a file named foo_ignore with the number of deleted rows prompted

    :param filename: File name
    :type filename: string
    :param ignore: Number of rows to be ignored
    :type ignore: int
    """
    with open(filename, "r") as cin, open(filename.replace(".csv","")+"_ignore.csv", "w+") as cout:
        fileOut = csv.writer(cout)
        for row in csv.reader(cin):
            if(ignore == 0):
                fileOut.writerow(row)
            else:
                ignore-=1
                
def createTemp():
    """Tests if the temp file already exists, if so do nothing
    otherwise, it will create a new one with min and max set to 0
    """
    try:
        open('data/temp.txt').readline()
        print((datetime.now()).strftime("[%H:%M:%S]"),"temp file already exists ! Nothing to do.")
        return
    except:
        file = open('data/temp.txt',"a+")
        file.write("min:0\nmax:0")
        file.close
        print("Created temp.txt. If a tweet was sent the data could be loss and it will be resent.")
                
def readTemp(text):
    """read the temp file for a certain line (min or max)

    :param text: "max" or "min", the line to read
    :type text: string
    :return: 1 or 0
    :rtype: int
    """
    with tryTemp() as file:
        match text:
            case "min":
                line=0
            case "max":
                line=1
            case _:
                print((datetime.now()).strftime("[%H:%M:%S]"),"'",text,"' is not in temp.txt")
                return
        return int(file.readlines()[line][4])

def setTemp(text,value):
    """set the value of certain line in the temp file

    :param text: "max" or "min", the line to read
    :type text: string
    :param value: 1 or 0
    :type value: int
    """
    with tryTemp() as file:
        match text:
            case "min":
                line=0
                tempText=file.readlines()[1-line]
                tempText="min:"+str(value)+"\n"+tempText
            case "max":
                line=1
                tempText=file.readlines()[1-line]
                tempText+="max:"+str(value)
            case _:
                print((datetime.now()).strftime("[%H:%M:%S]"),"'",text,"' is not in temp.txt")
                return
        readFile = file.readlines()
        file.seek(0)
        for line in readFile:
            file.truncate()
        file.write(tempText)

def tryTemp():
    """internal function, tests if the file exists or can be opened

    :return: file data with read/write permissions
    :rtype: file
    """
    try:
        open('data/temp.txt','r+').readlines()
        return open('data/temp.txt','r+')
    except:
        print((datetime.now()).strftime("[%H:%M:%S]"),"Can't open the file 'temp.txt, try creating one with createTemp()'")
        sys.exit()
