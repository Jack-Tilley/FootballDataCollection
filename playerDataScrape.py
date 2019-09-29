import csv
from bs4 import BeautifulSoup
import requests
import re

url = "https://en.wikipedia.org/wiki/"

def seturl(url,addition):
    addition = addition.replace(" ","_")
    newurl = url + addition
    return newurl


def playerinfoscrape(playerurl,soup,playerdob):
    playerdetails = []
    found = False
    if "Wikipedia does not have an article with this exact name." in soup.text:
        return None
    stop = 0
    while not found:
        if "Senior career*" not in soup.text:

            if soup.find("div", attrs={"class": "hatnote navigation-not-searchable"}) is not None: # on different persons page
                links = soup.find("div", attrs={"class": "hatnote navigation-not-searchable"}).find_all("a")
                for link in links:
                    if "footballer" in link.text or "disambiguation" in link.text:
                        soup = makesoup(url, link.text)
                # soup = makesoup(url, link)

            elif "may refer to:" in soup.find("div", attrs = {"class":"mw-parser-output"}).text \
                    or "is the name of:" in soup.find("div", attrs = {"class":"mw-parser-output"}).text \
                    or "may also refer to:" in soup.find("div", attrs = {"class":"mw-parser-output"}).text: # in disambiguation

                playeroptions = soup.find("div", attrs={"class": "mw-parser-output"}).find_all("li")
                playerlist = []
                isplayer = False
                for option in playeroptions:
                    if ("footballer" in option.text):# and (playerdob in option.text):
                        if playerdob in option.text:
                            link = option.find("a").text
                            soup = makesoup(url, link)
                            isplayer = True
                            break
                        else:
                            playerlist.append(option)
                if not isplayer:
                    for player in playerlist:
                        link = player.find("a").text
                        testsoup = makesoup(url, link)
                        if "Senior career*" in testsoup.text:
                            soup = testsoup
                            break

            else:
                return None # page not displayed correctly
        else:
            found = True
        if stop > 4:
            return None
        stop += 1

    playertables = soup.find_all("table", attrs={"class": "infobox vcard"})
    if len(playertables) == 1:
        playerrows = soup.find("table", attrs={"class": "infobox vcard"}).find_all("tr")
    else:
        for table in playertables:
            if "Senior career*" in table.text:
                playerrows = table.find_all("tr")

    i = 0
    start = 0

    for row in playerrows:
        if "Senior career*" in row.text:
            start = i+2
        elif "Total" in row.text:
            break
        elif "National team" in row.text:
            break
        elif "Teams managed" in row.text:
            break
        elif "* Senior club " in row.text:
            break
        elif "Signature" in row.text:
            break
        i += 1
    for line in range(start,i):
        clubhistory = playerrows[line].text.split("\n")[:2]
        clubhistory[1] = clubhistory[1].replace("→ ","")
        playerdetails.append(clubhistory)
    return playerdetails


def makesoup(url,playername):
    playerurl = seturl(url,playername)
    page = requests.get(playerurl)
    soup = BeautifulSoup(page.text, "html.parser")
    return soup


def getplayernames(playerData):
    playernames = []
    with open(playerData, 'r') as f:
        next(f)
        reader = csv.reader(f)
        for row in reader:
            playernames.append(row[0])
    return playernames


def getplayerbirthyear(playerData):
    playerdobs = []
    with open(playerData, 'r') as f:
        next(f)
        reader = csv.reader(f)
        for row in reader:
            playerdobs.append(row[2][-4:])
    return playerdobs


def getplayerid(playerData):
    playerids = []
    with open(playerData, 'r') as f:
        next(f)
        reader = csv.reader(f)
        for row in reader:
            playerids.append(row[3])
    return playerids


def tocsv(playerhistory):
    with open("playerTransferHistory", "a") as f:
        writer = csv.writer(f)
        writer.writerow(playerhistory)

# tocsv(["Name", "Country", "DoB","PlayerNo"])
def multiscrape(url, playerstart, playerend, playerData):
    playernames = getplayernames(playerData)
    playerdobs = getplayerbirthyear(playerData)
    playerids = getplayerid(playerData)
    for i in range(playerstart, playerend):
        playerid = playerids[playerstart]
        playername = playernames[playerstart]
        playerdob = playerdobs[playerstart]
        playerurl = seturl(url,playername)
        soup = makesoup(url, playername)
        playerhistory = playerinfoscrape(playerurl, soup, playerdob)
        if playerhistory is not None:
            for teamchange in playerhistory:
                teamchange.insert(0, playerid)
                tocsv(teamchange)
        playerstart+=1


#tocsv(["Name", "Club", "Date"])
#multiscrape(url,0,50000,"playerData.csv")
multiscrape(url,51101,51108,"playerDataWithId.csv")
#21440-21443