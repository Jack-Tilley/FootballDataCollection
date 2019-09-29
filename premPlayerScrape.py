from bs4 import BeautifulSoup
import requests
import time
import csv

premHtmlStart = "https://www.premierleague.com/players//player/overview"


# scrapes player name, player country, and player dob
def playerdetailscrape(soup,playerno):
    playerinfo = []

    playerdetails = soup.find("div", attrs={"class": "personalLists"})
    if playerdetails is not None:
            playerinfo.append(soup.find("div", attrs={"class": "playerDetails"}).text)
            playerinfo.append(playerdetails.find("span", attrs={"class": "playerCountry"}).text)
            try:
                playerinfo.append(playerdetails.find("ul", attrs={"class": "pdcol2"}).find("div", attrs={"class": "info"}).text)
            except AttributeError:
                playerinfo.append("TBD")
            playerinfo.append(playerno)

    return playerinfo


# changes the html to match the current player
def setplayerhtml(originalhtml, playerno):
    newhtml = originalhtml[:38] + str(playerno) + originalhtml[38:]
    return newhtml


# gathers player data from playervalue start to finalplayervalue end
def scrapecollect(originalhtml, playervalue, finalplayervalue):
    # playerslist = [["Name", "Country", "DoB","PlayerNo"]]
    for i in range(playervalue, finalplayervalue):
        html = setplayerhtml(originalhtml, i)
        page = requests.get(html)
        soup = BeautifulSoup(page.text, 'html.parser')

        playerinfolist = playerdetailscrape(soup, i)
        if playerinfolist:          # if list contains items:
            # playerslist.append(playerinfolist)
            tocsv(playerinfolist)
        time.sleep(1)

    # return playerslist


def tocsv(player):
    with open("players.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerow(player)

# tocsv(["Name", "Country", "DoB","PlayerNo"])

# measures time taken
start_time = time.time()
players = scrapecollect(premHtmlStart, 65001, 100000)
print("--- %s seconds ---" % (time.time() - start_time))










