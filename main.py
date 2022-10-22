#!/usr/bin/env python3
#!/usr/bin/env python2
from datetime import date
import tweepy
import config

from src.toulousenfeu import Toulousenfeu
from src.readfile import *
from src.connect import App
from src.twittertext import TwitterText

# App initialisation
app = App("Toulouse'n Feu")
app.setToken()
app.setURL()
app.connect()
# Tweepy initialisation
client = tweepy.Client(consumer_key=config.API_KEY,
                       consumer_secret=config.API_KEY_SECRET,
                       access_token=config.TOULOUSE_ACCESS_TOKEN,
                       access_token_secret=config.TOULOUSE_ACCESS_TOKEN_SECRET)

# Query informations and setting variables
tlf = Toulousenfeu(readFile("data/normales.csv"),readFile("data/export_infoclimat.csv",4,";"))
print("Normale Minimum :",tlf.moyNormale(date.today(),tlf.monthsNormalesMin))
print("Normale Maximum :",tlf.moyNormale(date.today(),tlf.monthsNormalesMax))
print("Minimum Aujourd'hui :",tlf.findMin())
print("Maximum Aujourd'hui :",tlf.findMax())

#Twitter bot
bot = TwitterText()
try :
    bot.emoji(tlf.findMin(),tlf.moyNormale(date.today(),tlf.monthsNormalesMin))
    bot.setText("min","La température minmale du "+ (date.today()).strftime("%d/%m/%Y") +" est de "+str(tlf.findMin())+"°C, soit "+tlf.diffNorm("min")+" par rapport à la normale. ("+bot.emojiContainer[0]+")")
    print(bot.textMin)
    response = client.create_tweet(text=bot.textMin)
    print(response)
except :
    print("Can't tweet min temp")
try:
    bot.emoji(tlf.findMax(),tlf.moyNormale(date.today(),tlf.monthsNormalesMax))
    bot.setText("max","La température maximale du "+ (date.today()).strftime("%d/%m/%Y") +" est de "+str(tlf.findMax())+"°C, soit "+tlf.diffNorm("max")+" par rapport à la normale. ("+bot.emojiContainer[1]+")")
    response = client.create_tweet(text=bot.textMax)
    print(response)
    print(bot.textMax)
except :
    print("Can't tweet max temp")