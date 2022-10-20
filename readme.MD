# Toulouse'n Feu !
## Purpose
Toulouse'n Feu is a Python app that aims to collect weather informations about today's global warming crisis. Because I *love* cold weather I realised that this autumn is quite hot. The idea of a Twitter bot that reminds everyday the insufficient suffering all human beings are living right now started to grow !\
Of Course it's not the only goal. I think it would be interesting to see if people are actually interested in this project, as well as showing datas everyday, and every month !
## Installation
To use this bot I recommend to install some python librairies such as :
>csv\
urllib.error\
datetime

Then, you'll have to create an account on [Infoclimat](https://www.infoclimat.fr/).\
Once created, go to this [link](https://www.infoclimat.fr/opendata/), paste your IP adress and generate a token key.\
![Infoclimat Token](/assets/infoclimattoken.png "Infoclimat's token creation")
#### Note : *Check that your IP address is static, otherwise the token key will have to be generated everytime your IP changes.*\
Then, create a text file named *key.txt* in the root directory. That's all ! You can launch your Python script and enjoy.
## Possible errors
```
[Toulouse'n Feu] : Can't open the file 'key.txt'
```
* The file key.txt isn't created, follow the steps in *Installation*

```
[Toulouse'n Feu] : HTTPError
[Toulouse'n Feu] : URLError
[Toulouse'n Feu] : Unexpected Error
```
* These come up when the connexion with Infoclimat can't be established. Or that the URL is not correct

```
[Toulouse'n Feu] : Wrong token id or ip address
```
* Be sure that your IP Address hasn't changed or that the token id have been correctly copied in the *key.txt* file
## Copyright
Data acquired with the help of [Infoclimat's opendata](https://www.infoclimat.fr/opendata/).\
Readme created with [Markdown Live Preview](https://markdownlivepreview.com/).