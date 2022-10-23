# Toulouse'n Feu !
## Purpose
Toulouse'n Feu is a Python app that aims to collect weather informations about today's global warming crisis. Because I *love* cold weather I realised that this autumn is quite hot. The idea of a Twitter bot that reminds everyday the insufficient suffering all human beings are living right now started to grow !\
Of course it's not gonna be the only goal. I think it would be interesting to see if people are actually interested in this project, as well as showing datas everyday, and every month !
## Datas returned
Toulouse'n Feu will return 4 values for the day :
>Minimum for today\
Minimum Normale Temp\
Maximum for today\
Maximum Normale Temp

Important note : the minimum is only set if a higher temperature is traced. The maximum temperature can't be set without the minimum.

It will then inform the state of the tweet. If it could be sent *(a temp file will be created and test if the tweet of today has already been sent)* or not, depending on the temp file or twitter in itself.

![Tweet example](/assets/twitterexample.png)

>Tweet example
## Installation
### Python
This bot uses some librairies that are not automatically installed on a clean python3 install. You can see the file [requirements](/requirements.txt) for a complete list.

### Tweepy
To actually send tweets the program uses the library [tweepy](https://pypi.org/project/tweepy/). You have to manually create a file named **config.py** with it, you will setup some variables like your API key, secret, and more importantly the Access token and secret.\
To generate the API Key you actually have to create a Twitter app from the [Twitter dev](https://developer.twitter.com/) page.

>**Your Twitter dev account doesn't have to be your bot's account**

To get the Access tokens, you can simply use yours, or install [twurl](https://github.com/twitter/twurl) and then follow its instructions. (The consumer key is the same as the API in their tutorial)

Finally you'll have to create some variables in the **config.py** :
```
API_KEY
API_KEY_SECRET
ACCESS_TOKEN
ACCESS_TOKEN_SECRET
```
### Acquire data
You'll have to create an account on [Infoclimat](https://www.infoclimat.fr/) and make it verified. Once created and verified, go to this [link](https://www.infoclimat.fr/opendata/), paste your IP address and generate a token key. I recommend you to fix your IP address as static. If it's a home server you are hosting, ask your operator.

![Infoclimat Token](/assets/infoclimattoken.png "Infoclimat's token creation")

Then, create a text file named *key.txt* in the **data** directory and paste your key into it.

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

>For **day** > **middleDay** of the month
```
(Tn)-((d - dM)/(dM + dM+1))*(Tn - TnM+1)
```
>For **middleDay** > **day** of the month
```
(TnM-1)-((d + dM-1)/(dM + dM-1))*(TnM-1 - Tn)
```
This formula over the year could look like this graph :

![Temp MIN MAX Normales](/assets/tempmin_max_normales.png "Temp MIN MAX Normales")
*Source: [MeteoFrance](https://donneespubliques.meteofrance.fr/?fond=produit&id_produit=117&id_rubrique=39)\
Every point is the middle of a month*
## Possible errors
```
[Toulouse'n Feu] : Can't open the file 'key.txt'
```
* The file data/key.txt isn't created, follow the steps in *Installation*

```
[Toulouse'n Feu] : HTTPError
[Toulouse'n Feu] : URLError
[Toulouse'n Feu] : Unexpected Error
```
* These come up when the connexion with Infoclimat can't be established. Or that the URL is not correct

```
[Toulouse'n Feu] : Wrong token id or ip address
```
* Be sure that your IP Address hasn't changed or that the token id have been correctly copied in the *data/key.txt* file
## Note to contributors
I'm using sphinx's docstring format. If you want to add any function be sure to check the [documentation](https://www.sphinx-doc.org/en/master/index.html)
## Copyright
Data acquired with the help of [Infoclimat's opendata](https://www.infoclimat.fr/opendata/).\
Normales Temperature are from [MeteoFrance's public library](https://donneespubliques.meteofrance.fr/?fond=produit&id_produit=117&id_rubrique=39).\
Readme created with [Markdown Preview Github Styling](https://github.com/mjbvz/vscode-github-markdown-preview-style).