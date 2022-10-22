import csv
import sys
from types import NoneType
import requests
from urllib.error import HTTPError, URLError
from datetime import date,timedelta
import calendar
from distro import info

# FUNCTIONS

def strZero(int):
    """Returns a string from an int, if it's < 10,
    It will add a zero in front of it.

    :param int: the integer you want to convert
    :type int: int
    :rtype: string
    """
    if int < 10:
        return "0"+str(int)
    return str(int)

def readFromTo(filename,list,ignore=0,Filedelimiter=","):
    """Read a CSV file and returns its content in the list

    :param filename: File name
    :type filename: string
    :param list: Empty list
    :type list: list
    :param ignore: raws to ignore in the file, defaults to 0
    :type ignore: int, optional
    :param Filedelimiter: Delimits the csv's columns, defaults to ","
    :type Filedelimiter: str, optional
    """
    if ignore > 0:
        deleteRow(filename,ignore)
        filename=filename.replace(".csv","")+"_ignore.csv"
    with open(filename, "r") as file:
        readerObj = csv.DictReader(file, delimiter=Filedelimiter)
        for row in readerObj:
            list.append(dict(row))

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

def getNormales(column,month):
    """Get the normales from a specified month.
    The list "tempNormales" needs to be created.

    :param column: Temp,MaxTemp,MaxTempDate,MinTemp,MinTempDate
    :type column: string
    :param month: The month you want to strip datas
    :type month: int
    :return: the specified term in the csv
    :rtype: string
    """
    for row in tempNormales:
        if int(row["Month"]) == month:
            return row[column]

def getTodayTemps():
    """Get the temperatures at a given day, in form of a list.
    Every 3 hours.
    The list "infoClimat" needs to be created.

    :rtype: list of string
    """
    returnValue = []
    for i in range(0, 22, 3):
        todayDate = (date.today()).strftime("%Y-%m-%d ")+strZero(i)+":00:00"
        for row in infoClimat:
            if row["dh_utc"] == todayDate:
                returnValue.append(row["temperature"])
    return returnValue

def moyNormale(givenDate,listTempMonth):
    """Get the medium for a list of the current day

    :param givenDate: a given date
    :type givenDate: date
    :param listTempMonth: the list of temps in 12 months (0 to 11)
    :type listTempMonth: list of strings
    :rtype: float
    """
    monthMaxDay = calendar.monthrange(givenDate.year, givenDate.month)[1]
    midMonthMaxDay = monthMaxDay/2
    if (monthMaxDay - givenDate.day) < midMonthMaxDay:
        midNextMonth = (calendar.monthrange(givenDate.year, givenDate.month)[1])/2
        return float(listTempMonth[int2month(givenDate.month-1)])-((givenDate.day-midMonthMaxDay)/(midNextMonth+midMonthMaxDay))*(float(listTempMonth[int2month(givenDate.month-1)])-float(listTempMonth[int2month(givenDate.month)]))
    else:
        midBeforeMonth = (calendar.monthrange(givenDate.year, givenDate.month)[1])/2
        return float(listTempMonth[int2month(givenDate.month-2)])-((givenDate.day+midBeforeMonth)/(midBeforeMonth+midMonthMaxDay)*(float(listTempMonth[int2month(givenDate.month-2)])-float(listTempMonth[int2month(givenDate.month-1)])))

def int2month(num):
    """Convert a int to a month (number between 0-11)

    :param num: number given
    :type num: int
    :return: month between 0 and 11
    :rtype: int
    """
    if num<0:
        return 12+num
    elif num>11:
        return num-12
    return num

def findMin(list):
    """find the minimum term of the following list
    If the list finish with the minimum number, returns none
    It creates a global variable called minListRow, which is
    the row of the list containing the minimum value.

    :param list: list cotaining more than 1 term, with one term higher than the minimum value
    :type list: list of string
    :return: the minimum value
    :rtype: float
    """
    global minListRow
    minListRow = 0
    try :
        originTemp = float(list[0])
    except :
        return
    for temps in list:
        while originTemp>float(temps):
            originTemp = float(temps)
            minListRow+=1
    try :
        list[minListRow+1]
        return originTemp
    except :
        return
    
def findMax(list,iterate):
    """Depends on findMin(), find the maximum value after the minimum

    :param list: list cotaining more than 1 term, with the minimum value and a term lower than the maximum value
    :type list: list of string
    :param iterate: minListRow, the function starts at the minimum value
    :type iterate: int
    :return: the maximum value
    :rtype: float
    """
    min = findMin(list)
    if type(min) == NoneType :
        return
    for temps in list[minListRow:]:
        while min<float(temps):
            min = float(temps)
            iterate+=1
    try :
        list[iterate+1]
        return min
    except :
        return

# MAIN

# query the token id from the text file
appName="Toulouse'n Feu"
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
monthsNormales = []
monthsNormalesMin = []
monthsNormalesMax = []

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

# sets up the lists of temperature, normales for today
readFromTo("normales.csv",tempNormales)
readFromTo("export_infoclimat.csv",infoClimat,4,";")
for i in range(1,13):
    monthsNormales.append(getNormales('Temp',i))
    monthsNormalesMin.append(getNormales('MoyTempMin',i))
    monthsNormalesMax.append(getNormales('MoyTempMax',i))

# Main
print("Normale Minimum :",moyNormale(date.today(),monthsNormalesMin))
print("Normale Maximum :",moyNormale(date.today(),monthsNormalesMax))
print("Minimum Aujourd'hui :",findMin(getTodayTemps()))
print("Maximum Aujourd'hui :",findMax(getTodayTemps(),minListRow))