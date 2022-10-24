import sys
from datetime import date,datetime
import requests
from urllib.error import HTTPError, URLError

class App():
    def __init__(self, appName):
        self.appName = appName
        
    def setToken(self):
        """
        set the Token from key.txt
        """
        try :
            self.tokenId = open('data/key.txt').readline()
        except OSError:
            print((datetime.now()).strftime("[%H:%M:%S]"),"["+self.appName+"] : Can't open the file 'key.txt'")
            sys.exit()

    def setURL(self):
        """
        Setup the URL with the date of today
        """
        today = (date.today()).strftime("%Y-%m-%d")
        self.URL = "https://www.infoclimat.fr/opendata/?method=get&format=csv&stations[]=07630&start="+today+"&end="+today+"&token="+self.tokenId
        
    def connect(self):
        """
        Save the infoclimat file with the given URL
        """
        try :
            open("data/export_infoclimat.csv", "wb").write((requests.get(self.URL)).content)
        except HTTPError as e:
            print((datetime.now()).strftime("[%H:%M:%S]"),"["+self.appName+"] : HTTPError ("+str(e)+")")
            sys.exit()
        except URLError as e:
            print((datetime.now()).strftime("[%H:%M:%S]"),"["+self.appName+"] : URLError ("+str(e)+")")
            sys.exit()
        except NameError :
            print((datetime.now()).strftime("[%H:%M:%S]"),"["+self.appName+"] : URL not set")
            sys.exit()
        except Exception as e:
            print((datetime.now()).strftime("[%H:%M:%S]"),"["+self.appName+"] : Unexpected Error ("+str(e)+")")
            sys.exit()
        if open('data/export_infoclimat.csv').readline() != "# METADATA:\n":
            print((datetime.now()).strftime("[%H:%M:%S]"),"["+self.appName+"] : Wrong token id or ip address")
            sys.exit()