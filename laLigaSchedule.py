from bs4 import BeautifulSoup
import requests
import time
import csv
import datetime
import os
from selenium import webdriver

laLigaHtmlStart = "https://www.laliga.es/en/statistics-historical/calendar/primera//"
start = "1928-29"
page = requests.get("https://www.laliga.es/en/statistics-historical/calendar/primera/1928-29/")
soup = BeautifulSoup(page.text, "html.parser")
matchdays = soup.find_all("div", attrs={"class": "jornada-calendario-historico"})

# teams = []
def scheduleScrape(soup,startyear,url):
    gameno = 0
    week = 0
    season = []
    season_id = startyear[:4]
    matchdays = soup.find_all("div", attrs={"class": "jornada-calendario-historico"})

    driver = webdriver.Chrome('/Users/Tilley/Downloads/chromedriver')
    driver.get(url)
    time.sleep(1)
    innerHTML = driver.execute_script("return document.body.innerHTML")
    driversoup = BeautifulSoup(innerHTML, "html.parser")
    time.sleep(5)
    driver.find_element_by_xpath('//*[contains(@class,"optanon-alert-box-close")]').click()
    drivergame = driver.find_elements_by_tag_name("tr")


    for matchday in matchdays:
        week +=1
        # date = matchday.find("div", attrs={"class": "nombre_jornada"}).text[-10:].strip()
        # date = dateformat(date)
        games = matchday.find_all("tr")
        for game in games:
            gameinfo = []

            time.sleep(1)
            drivergame[gameno].click()
            time.sleep(1)
            innerHTML = driver.execute_script("return document.body.innerHTML")
            time.sleep(1)
            scope = BeautifulSoup(innerHTML, "html.parser")
            x = scope.find("div", attrs={"id": "contenedor_titulo"}).find_all("div")
            date = x[2].text.split()[1].strip(".")
            driver.find_element_by_xpath('//a[@href="'"javascript:;"'"]').click()
            time.sleep(1)

            date = dateformat(date)
            scores = game.find_all("b")
            score1 = scores[0].text
            score2 = scores[1].text
            score = score1 + "-" + score2
            match = game.text.replace(score1,"").replace(score2, "").split(":")[:-1]
            match[1] = match[1].lstrip()
            team1 = match[0]
            # if team1 not in teams:
            #     teams.append(team1)
            team1 = namechanges(team1)
            team1 = team1 + " (" + str(week) + ")"
            team2 = match[1]
            team2 = namechanges(team2)
            team2 = team2 + " (" + str(week) + ")"
            gameinfo.append("?")
            gameinfo.append(date)
            gameinfo.append(team1)
            gameinfo.append(score)
            gameinfo.append("?")
            gameinfo.append(team2)
            # gameinfo.append(season_id)
            season.append(gameinfo)
            gameno += 1
    return season


def setyear(html, season):
    seasonend = int(season) + 1
    seasonend = str(seasonend)
    seasonend = seasonend[-2:]
    fullhtml = html[:-1] + season + "-" + seasonend + html[-1:]
    return fullhtml


def fullscrape(orightml,seasonstart,seasonend):
    teams = []
    for i in range(int(seasonstart[:4]),int(seasonend[:4])):
        seasonhtml = setyear(orightml, str(i))
        page = requests.get(seasonhtml)
        soup = BeautifulSoup(page.text, 'html.parser')

        fullseason = scheduleScrape(soup, str(i), seasonhtml)
        tocsv(str(i), fullseason)


def tocsv(season_title, fullseason):
    seasonend = int(season_title) +1
    seasonend = str(seasonend)[-2:]
    dir = "/Users/Tilley/Desktop/spaintest3/" +season_title +"-" + seasonend + "/"
    if not os.path.exists(dir):
        os.makedirs(dir)
    with open(dir + "1-liga.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows([["Round", "Date", "Team 1", "FT", "HT", "Team 2"]])
        writer.writerows(fullseason)


def dateformat(date):
    dateformat = "%d/%m/%Y"
    newformat = "(%a) %-d %b %Y (%-W)"
    formatteddate = datetime.datetime.strptime(date, dateformat).strftime(newformat)
    return formatteddate

def namechanges(teamName):
    teams = {
        "Athletic Club": "Athletic Club Bilbao",
        "Atlético de Madrid": "Atlético Madrid",
        "Real Madrid": "Real Madrid CF",
        "R. Racing C": "Real Racing Santander",
        "Albacete BP": "Albacete Balompié",
        "C.A. Osasuna": "CA Osasuna",
        "R. Zaragoza": "Real Zaragoza",
        "RCD Espanyol": "RCD Español",
        "CD Málaga": "Málaga CF",
        "D. Alavés": "Deportivo Alavés",
        "Elche C.F.": "Elche CF",
        "RC Celta": "RC Celta Vigo",
        "Real Murcia": "Real Murcia CF",
        "R. Oviedo": "Real Oviedo",
        "R. Valladolid CF": "Real Valladolid CF",
        "RC Recreativo": "Recreativo Huelva",
        "Salamanca": "UD Salamanca",
        "AD Almería": "UD Almería",
        "Lleida Esportiu": "UE Lleida",
        "Nàstic": "Gimnàstic Tarragona",
        "RC Deportivo": "RCD La Coruña"
    }
    newName = teamName
    if teamName in teams:
        newName = teams.get(teamName)
    return newName




fullscrape(laLigaHtmlStart, "1992-93", "1994-95")


