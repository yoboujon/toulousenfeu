import csv

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
