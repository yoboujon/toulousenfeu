from datetime import datetime

class TwitterText:
    def __init__(self):
        self.emojiContainer = []   
         
    def emoji(self,todayTemp,normaleTemp):
        """Sets the number of emoji for this day in a container

        :param todayTemp: temperature of today
        :type todayTemp: int/float
        :param normaleTemp: normale temperature
        :type normaleTemp: int/float
        """
        emojiTemp = ""
        try :
            if todayTemp > normaleTemp:
                while normaleTemp < todayTemp:
                    emojiTemp+="🔥️"
                    todayTemp-=3
                self.emojiContainer.append(emojiTemp)
                return
            else:
                while normaleTemp > todayTemp:
                    emojiTemp+="🧊️"
                    todayTemp+=3
                self.emojiContainer.append(emojiTemp)
        except:
            return
        
    def setText(self,minMax,text):
        try:
            match minMax:
                case "min":
                    self.textMin=text
                case "max":
                    self.textMax=text
                case _:
                    print((datetime.now()).strftime("[%H:%M:%S]"),"No matched name for: ",minMax)
                    return
        except:
            return