#!/usr/bin/env python3
#!/usr/bin/env python2
from datetime import date,datetime
import time
import tweepy
import config

from src.toulousenfeu import Toulousenfeu
from src.readfile import *
from src.connect import App
from src.twittertext import TwitterText

def Run():
    """Main function
    """

    # Temp file initialisation/sleep
    createTemp()
    actualHour = datetime.now().hour
    if actualHour <= 2 and actualHour >= 0:
        setTemp("min",0)
        setTemp("max",0)
        print((datetime.now()).strftime("[%H:%M:%S]"),"temp.txt has been reset because we are between 12 PM and 3 AM, the program will now shutdown")
        return
    # App initialisation
    app = App("Toulouse'n Feu")
    app.setToken()
    app.setURL()
    app.connect()
    # Tweepy initialisation
    client = tweepy.Client(consumer_key=config.API_KEY,
                        consumer_secret=config.API_KEY_SECRET,
                        access_token=config.ACCESS_TOKEN,
                        access_token_secret=config.ACCESS_TOKEN_SECRET)

    # Query informations and setting variables
    tlf = Toulousenfeu(readFile("data/normales.csv"),readFile("data/export_infoclimat.csv",4,";"))

    #Twitter bot
    bot = TwitterText()
    maxContainer = 0

    try :
        if readTemp("min")==0:
            print((datetime.now()).strftime("[%H:%M:%S]"),"Normale Minimum :",tlf.moyNormale(date.today(),tlf.monthsNormalesMin))
            print((datetime.now()).strftime("[%H:%M:%S]"),"Minimum Aujourd'hui :",tlf.findMin())
            bot.emoji(tlf.findMin(),tlf.moyNormale(date.today(),tlf.monthsNormalesMin))
            bot.setText("min","La température minimale du "+ (date.today()).strftime("%d/%m/%Y") +" est de "+str(tlf.findMin())+"°C, soit "+tlf.diffNorm("min")+" par rapport à la normale. ("+bot.emojiContainer[0]+")")
            print((datetime.now()).strftime("[%H:%M:%S] Min Tweet to send : "),bot.textMin)
            response = client.create_tweet(text=bot.textMin)
            print((datetime.now()).strftime("[%H:%M:%S]"),response)
            setTemp("min",1)
            if readTemp("max")==0:
                maxContainer = 1
        else:
            print((datetime.now()).strftime("[%H:%M:%S]"),"Tweet for min already sent.")
    except :
        print((datetime.now()).strftime("[%H:%M:%S]"),"Can't tweet min temp yet")
    try:
        if readTemp("max")==0:
            print((datetime.now()).strftime("[%H:%M:%S]"),"Normale Maximum :",tlf.moyNormale(date.today(),tlf.monthsNormalesMax))
            print((datetime.now()).strftime("[%H:%M:%S]"),"Maximum Aujourd'hui :",tlf.findMax())
            bot.emoji(tlf.findMax(),tlf.moyNormale(date.today(),tlf.monthsNormalesMax))
            bot.setText("max","La température maximale du "+ (date.today()).strftime("%d/%m/%Y") +" est de "+str(tlf.findMax())+"°C, soit "+tlf.diffNorm("max")+" par rapport à la normale. ("+bot.emojiContainer[maxContainer]+")")
            print((datetime.now()).strftime("[%H:%M:%S] Max Tweet to send : "),bot.textMax)
            response = client.create_tweet(text=bot.textMax)
            print((datetime.now()).strftime("[%H:%M:%S]"),response)
            setTemp("max",1)
        else:
            print((datetime.now()).strftime("[%H:%M:%S]"),"Tweet for max already sent.")
    except :
        print((datetime.now()).strftime("[%H:%M:%S]"),"Can't tweet max temp yet")

Run()
while True:
    now = datetime.now()
    if now.minute==45 or now.minute==15:
        Run()
        time.sleep(60)
    else:
        time.sleep(30)