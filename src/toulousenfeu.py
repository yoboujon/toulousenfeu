from datetime import date
import calendar
from types import NoneType
from . import convert

class Toulousenfeu():
    """
    Toulousenfeu main class, requires infoclimat and normales lists
    From these, will create monthsNormales, min, max, lists of normales temperature, string format
    getNormales with a column and a month will get the specified normale
    
    """
    def __init__(self, tempNormales,infoClimat):
        self.tempNormales = tempNormales
        self.infoClimat = infoClimat
        self.monthsNormales = []
        self.monthsNormalesMin = []
        self.monthsNormalesMax = []
        for i in range(1,13):
            self.monthsNormales.append(self.getNormales('Temp',i))
            self.monthsNormalesMin.append(self.getNormales('MoyTempMin',i))
            self.monthsNormalesMax.append(self.getNormales('MoyTempMax',i))
        
    def getNormales(self, column,month):
        """Get the normales from a specified month.
        The list "tempNormales" needs to be created.

        :param column: Temp,MaxTemp,MaxTempDate,MinTemp,MinTempDate
        :type column: string
        :param month: The month you want to strip datas
        :type month: int
        :return: the specified term in the csv
        :rtype: string
        """
        for row in self.tempNormales:
            if int(row["Month"]) == month:
                return row[column]

    def getTodayTemps(self):
        """Get the temperatures at a given day, in form of a list.
        Every 3 hours.
        The list "infoClimat" needs to be created.

        :rtype: list of string
        """
        returnValue = []
        for i in range(0, 22, 3):
            todayDate = (date.today()).strftime("%Y-%m-%d ")+convert.strZero(i)+":00:00"
            for row in self.infoClimat:
                if row["dh_utc"] == todayDate:
                    returnValue.append(row["temperature"])
        return returnValue

    def moyNormale(self, givenDate,listTempMonth):
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
            return float(listTempMonth[convert.int2month(givenDate.month-1)])-((givenDate.day-midMonthMaxDay)/(midNextMonth+midMonthMaxDay))*(float(listTempMonth[convert.int2month(givenDate.month-1)])-float(listTempMonth[convert.int2month(givenDate.month)]))
        else:
            midBeforeMonth = (calendar.monthrange(givenDate.year, givenDate.month)[1])/2
            return float(listTempMonth[convert.int2month(givenDate.month-2)])-((givenDate.day+midBeforeMonth)/(midBeforeMonth+midMonthMaxDay)*(float(listTempMonth[convert.int2month(givenDate.month-2)])-float(listTempMonth[convert.int2month(givenDate.month-1)])))

    def findMin(self):
        """find the minimum term of the following list
        If the list finish with the minimum number, returns none
        It creates a global variable called minListRow, which is
        the row of the list containing the minimum value.

        :param list: list cotaining more than 1 term, with one term higher than the minimum value
        :type list: list of string
        :return: the minimum value
        :rtype: float
        """
        self.minListRow=0
        list = self.getTodayTemps()
        try :
            originTemp = float(list[0])
        except :
            return
        for temps in list:
            while originTemp>float(temps):
                originTemp = float(temps)
                self.minListRow+=1
        try :
            list[self.minListRow+1]
            return originTemp
        except :
            return
        
    def findMax(self):
        """Depends on findMin(), find the maximum value after the minimum

        :param list: list cotaining more than 1 term, with the minimum value and a term lower than the maximum value
        :type list: list of string
        :param iterate: minListRow, the function starts at the minimum value
        :type iterate: int
        :return: the maximum value
        :rtype: float
        """
        list = self.getTodayTemps()
        min = self.findMin()
        iterate = self.minListRow
        if type(min) == NoneType :
            return
        for temps in list[self.minListRow:]:
            while min<float(temps):
                min = float(temps)
                iterate+=1
        try :
            list[iterate+1]
            return min
        except :
            return
        
    def diffNorm(self,text):
        """Difference between today's temperature and the normale of the month

        :param text: "min" or "max"
        :type text: string
        :rtype: float
        """
        operator = ""
        try:
            match text:
                case "min":
                    normale = self.moyNormale(date.today(),self.monthsNormalesMin)
                    tempReturn = self.findMin()
                case "max":
                    normale = self.moyNormale(date.today(),self.monthsNormalesMax)
                    tempReturn = self.findMax()
                case _:
                    print("No matched name for: ",text)
                    return
            if tempReturn > normale:
                operator="+"
            return (operator+"{:.2f}".format(tempReturn-normale))
        except:
            return