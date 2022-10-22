# Toulouse'n Feu !
## Purpose
Toulouse'n Feu is a Python app that aims to collect weather informations about today's global warming crisis. Because I *love* cold weather I realised that this autumn is quite hot. The idea of a Twitter bot that reminds everyday the insufficient suffering all human beings are living right now started to grow !\
Of course it's not gonna be the only goal. I think it would be interesting to see if people are actually interested in this project, as well as showing datas everyday, and every month !
## Datas returned
Toulouse'n Feu will return 4 values for the day :
>Minimum Normale Temp\
Maximum Normale Temp\
Maximum for today\
Minimum for today

Important note : the minimum is only set if a higher temperature is traced. The maximum temperature can't be set without the minimum.
## Installation
To use this bot I recommend to install some python librairies with pip such as :
>csv\
urllib.error\
datetime\
calendar

Then, you'll have to create an account on [Infoclimat](https://www.infoclimat.fr/) and make it verified.\
Once created and verified, go to this [link](https://www.infoclimat.fr/opendata/), paste your IP address and generate a token key.\
![Infoclimat Token](/assets/infoclimattoken.png "Infoclimat's token creation")
#### Note : *Check that your IP address is static, otherwise the token key will have to be generated everytime your IP changes.*
Then, create a text file named *key.txt* in the root directory. That's all ! You can launch your Python script and enjoy.
## Calculating the Normales
The normales for both maximum and minimum temperatures come from the [MeteoFrance](https://donneespubliques.meteofrance.fr/?fond=produit&id_produit=117&id_rubrique=39)'s website. Unfortunetly I only had access to the datas from 1991 to 2020. Which i'm **sure** are way higher than 10 years before.\
Contrary to *Infoclimat* I will not compare today's temperatures to the normales of the month. Instead, I will be using an approximation with proportionnality. Every normales are set to the middle of each month. I joint every point using a basic formula :
| Names                            | Formula       |
| -------------------------------- |:-------------:|
| Next Month's Normale             | TnM+1         |
| Previous Month's Normale         | TnM-1         |
| Actual Month's Normale           | Tn            |
| Day                              | d             |
| Middle day of the month          | dM            |
| Middle day of the previous month | dM-1          |
| Middle day of the next month     | dM+1          |
```
(Tn)-((d - dM)/(dM + dM+1))*(Tn - TnM+1)
```
<div style="text-align: right">For <b>day</b> > <b>middleDay</b> of the month</div>

```
(TnM-1)-((d + dM-1)/(dM + dM-1))*(TnM-1 - Tn)
```
<div style="text-align: right">For <b>middleDay</b> > <b>day</b> of the month</div>

This formula over the year could look like this graph :
![Temp MIN MAX Normales](/assets/tempmin_max_normales.png "Temp MIN MAX Normales")
*Source: [MeteoFrance](https://donneespubliques.meteofrance.fr/?fond=produit&id_produit=117&id_rubrique=39)\
Every point is the middle of a month*
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
## Note to contributors
I'm using sphinx's docstring format. If you want to add any function be sure to check the [documentation](https://www.sphinx-doc.org/en/master/index.html)
## Copyright
Data acquired with the help of [Infoclimat's opendata](https://www.infoclimat.fr/opendata/).\
Normales Temperature are from [MeteoFrance's public library](https://donneespubliques.meteofrance.fr/?fond=produit&id_produit=117&id_rubrique=39).\
Readme created with [Markdown Preview Github Styling](https://github.com/mjbvz/vscode-github-markdown-preview-style).