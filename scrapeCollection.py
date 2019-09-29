from selenium import webdriver
import time
from bs4 import BeautifulSoup
import re
import datetime
import requests

outPutDateFormat = "%Y/%m/%d"
class ScheduleCollection:
    def __init__(self):
        print("hello")



    def bundScrape(self):
        # working perfectly
        bundURL = "https://www.bundesliga.com/en/bundesliga/matchday/2018-2019/?d=1"
        driverBund = webdriver.Chrome('/Users/Tilley/Downloads/chromedriver')
        schedule = []
        for i in range(2, 36):  # 35 for full schedule
            driverBund.get(bundURL)
            time.sleep(1)

            innerHTML = driverBund.execute_script("return document.body.innerHTML")

            soup = BeautifulSoup(innerHTML, "html.parser")

            scope = soup.find("div", attrs={"class": "panel buli-fixtures"})

            matchDaySet = True
            matchNotScheduled = scope.find("div", attrs={"class": "panel-heading fixtures20ActMatchdayNotFixed"})
            try:
                matchNotScheduled = matchNotScheduled.text
            except:
                pass
            if type(matchNotScheduled) is str:
                matchDaySet = False
                hiddenDate = scope.find("div", attrs={"class": "panel-heading fixtures20ActMatchdayRange hidden"})

            games = scope.find_all("div", attrs={"id": re.compile("^fixtures_DFL-MAT")})
            week = []
            for game in games:
                fixture = []
                homeTeam = game.find("td", attrs={"class": "fixtures-home"}).text
                result = game.find("td", attrs={"class": "fixtures-result"}).text
                awayTeam = game.find("td", attrs={"class": "fixtures-away"}).text

                if matchDaySet == True:
                    dateTime = game.find_previous_sibling("div", attrs={"class": "panel-heading"}).text.split("|")
                    date = dateTime[0]
                    gameTime = dateTime[1]
                else:
                    date = hiddenDate.text
                    gameTime = "9:30"
                dateparts = date.strip().split()
                date = dateparts[1]
                result = result[0:5]
                fixture.append(homeTeam)
                fixture.append(awayTeam)
                fixture.append(result)
                fixture.append(date)
                fixture.append(gameTime)
                week.append(fixture)
            schedule.append(week)

            if i < 11:
                bundURL = bundURL[:-1]
            else:
                bundURL = bundURL[:-2]
            bundURL = bundURL + str(i)
        dateFormat = "%m/%d/%Y"
        for matchweek in schedule:
            for game in matchweek:
                game[3] = datetime.datetime.strptime(game[3], dateFormat)
                game[3] = str(datetime.date.strftime(game[3], outPutDateFormat))

        return schedule

    def premScrape(self):
        ##works correctly
        ##gets all remaining fixtures
        ##fixtures picks up where scores left off
        url = "https://www.premierleague.com/fixtures/"
        driver = webdriver.Chrome('/Users/Tilley/Downloads/chromedriver')
        driver.get(url)
        time.sleep(1)

        SCROLL_PAUSE_TIME = 0.5
        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)
            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        innerHTML = driver.execute_script("return document.body.innerHTML")
        time.sleep(3)
        soup = BeautifulSoup(innerHTML, "html.parser")

        SCROLL_PAUSE_TIME = 0.5

        time.sleep(10)
        # find div data competition matches list for date, then look inside for games correlating to date
        dates = soup.find_all("time", attrs={"class": "date long"})
        gameDates = []
        for date in dates:
            date = date.text
            gameDates.append(date)

        fixtures = []
        for date in gameDates:
            gamesToday = soup.find("div", attrs={"data-competition-matches-list": date})
            gamesToday = gamesToday.find_all("li", attrs={"class": "matchFixtureContainer"})
            for game in gamesToday:
                aGame = game.text
                aGame = aGame.strip()
                aGame = aGame.split("  ")
                aGame = [x for x in aGame if x]
                aGame = aGame[0:3]
                aGame.append(date)
                fixtures.append(aGame)

        # gets result of matches played
        # these are basically 2 seperate programs
        url = "https://www.premierleague.com/results"
        driver = webdriver.Chrome('/Users/Tilley/Downloads/chromedriver')
        driver.get(url)
        time.sleep(10)

        innerHTML = driver.execute_script("return document.body.innerHTML")

        soup = BeautifulSoup(innerHTML, "html.parser")

        scope = soup.find("section", attrs={"class": "fixtures"})
        theDates = scope.find_all("div", attrs={"data-competition-matches-list": True})
        scores = []
        for date in theDates:
            x = date.get("data-competition-matches-list")
            aDay = date.find("ul", attrs={"class": "matchList"})
            completedMatches = aDay.find_all("li", attrs={"class": "matchFixtureContainer"})
            for match in completedMatches:
                matchInfo = match.text.strip().split("  ")[0:3]
                matchInfo.append(x)
                scores.append(matchInfo)
        scores = scores[::-1]
        # this combines the two but could give some bugs if the two pages arent in sync
        for element in fixtures:
            scores.append(element)
        wholeSchedule = scores
        for element in wholeSchedule:
            element[1], element[2] = element[2], element[1]
        dateFormat = "%A,%d,%B,%Y"
        for element in wholeSchedule:
            element[3] = element[3].replace(" ", ",")
            element[3] = datetime.datetime.strptime(element[3], dateFormat)
            element[3] = str(datetime.date.strftime(element[3], outPutDateFormat))

        return wholeSchedule

    def ligueScrape(self):
        # completed totally

        lig1Url = "https://www.ligue1.com/ligue1/calendrier_resultat#sai=102&jour=1"
        driverlig1 = webdriver.Chrome('/Users/Tilley/Downloads/chromedriver')
        schedule = []
        for i in range(38):  # 38 for full
            driverlig1.get(lig1Url)
            time.sleep(1)
            innerHTML = driverlig1.execute_script("return document.body.innerHTML")

            soup = BeautifulSoup(innerHTML, "html.parser")

            scope = soup.find("div", attrs={"id": "tableaux_rencontres"})
            gameDays = scope.find_all("tbody")

            theDates = scope.find_all("h4")  # used to give dates to every game in following for clause
            n = 0

            matchWeek = []
            for gameDay in gameDays:
                games = gameDay.find_all("tr")
                date = theDates[n].text
                n += 1
                for game in games:
                    match = []
                    gameTime = game.find("td", attrs={"class": "horaire "}).text
                    homeTeam = game.find("td", attrs={"class": "domicile"}).text.strip()
                    awayTeam = game.find("td", attrs={"class": "exterieur"}).text.strip()
                    result = game.find("td", attrs={"class": "stats"}).text.strip()
                    match.append(homeTeam)
                    match.append(awayTeam)
                    match.append(result)
                    match.append(gameTime)
                    match.append(date)
                    matchWeek.append(match)

            schedule.append(matchWeek)
            if i < 9:
                lig1Url = lig1Url[:-1]
            else:
                lig1Url = lig1Url[:-2]
            lig1Url = lig1Url + str(i + 2)
        dateFormat = "%A,%d,%B,%Y"
        for element in schedule:
            element[3] = element[3].replace(" ", ",")
            element[3] = datetime.datetime.strptime(element[3], dateFormat)
            element[3] = str(datetime.date.strftime(element[3], outPutDateFormat))

        return schedule

    def calcioScrape(self):
        # working perfectly
        calAUrl = "http://www.legaseriea.it/en/serie-a/fixture-and-results/2018-19/UNICO/UNI/1"
        driverCalA = webdriver.Chrome('/Users/Tilley/Downloads/chromedriver')
        schedule = []
        for i in range(38):  # 37 or #39???
            driverCalA.get(calAUrl)
            time.sleep(1)
            innerHTML = driverCalA.execute_script("return document.body.innerHTML")
            soup = BeautifulSoup(innerHTML, "html.parser")

            scope = soup.find("section", attrs={"class": "risultati"})
            gamesThisWeek = scope.find_all("div", attrs={"class": re.compile("^box-partita")})
            matchWeek = []
            for game in gamesThisWeek:
                match = []
                dateTime = game.find("div", attrs={"class": "datipartita"}).find("span").text.split()
                homeTeam = game.find("div", attrs={"class": re.compile("^col-xs-6 risultatosx")})
                homeName = homeTeam.find("h4", attrs={"class": "nomesquadra"}).text
                homeScore = homeTeam.find("span").text
                awayTeam = game.find("div", attrs={"class": re.compile("^col-xs-6 risultatodx")})
                awayName = awayTeam.find("h4", attrs={"class": "nomesquadra"}).text
                awayScore = awayTeam.find("span").text
                if len(dateTime) == 2:
                    date = dateTime[0]
                    gameTime = dateTime[1]
                else:
                    date = dateTime[0]
                    gameTime = None
                result = homeScore + "-" + awayScore
                match.append(homeName)
                match.append(awayName)
                match.append(result)
                match.append(date)
                match.append(gameTime)
                matchWeek.append(match)
            schedule.append(matchWeek)
            if i < 9:
                calAUrl = calAUrl[:-1]
            else:
                calAUrl = calAUrl[:-2]
            calAUrl = calAUrl + str(i + 2)
        dateFormat = "%d/%m/%Y"
        for matchweek in schedule:
            for game in matchweek:
                game[3] = datetime.datetime.strptime(game[3], dateFormat)
                game[3] = str(datetime.date.strftime(game[3], outPutDateFormat))
        return schedule


    def championsleaguegroupdrawscrape(self):
        # maybe this belongs somewhere else
        groupsURL = "https://www.uefa.com/uefachampionsleague/season=2019/matches/#/dw/1141"
        driverCL = webdriver.Chrome('/Users/Tilley/Downloads/chromedriver')
        driverCL.get(groupsURL)
        time.sleep(1)
        innerHTML = driverCL.execute_script("return document.body.innerHTML")
        soup = BeautifulSoup(innerHTML, "html.parser")
        scope = soup.find("div", attrs={"class":"draw-wrap draw-Group row"})
        groups = scope.find_all("div", attrs={"class": "col-xs-12 col-sm-6 col-md-3"})
        fullGroup = []
        for group in groups:
            theGroup = []
            groupLetter = group.find("h4", attrs={"class":"draw-list-title"}).text
            teamsInGroup = group.find_all("li", attrs={"class":"draw-list-item"})
            theGroup.append(groupLetter)
            for team in teamsInGroup:
                groupTeam = team.text.strip().replace("\n","")
                theGroup.append(groupTeam)
            fullGroup.append(theGroup)
        return fullGroup

    def championsleaguegroupgames(self):
        clURL = "https://www.uefa.com/uefachampionsleague/season=2019/matches/#/md/33574"
        driverCL = webdriver.Chrome('/Users/Tilley/Downloads/chromedriver')
        schedule = []
        for i in range(6): #6
            driverCL.get(clURL)
            time.sleep(1)
            innerHTML = driverCL.execute_script("return document.body.innerHTML")
            soup = BeautifulSoup(innerHTML, "html.parser")
            scope = soup.find("div", attrs={"class": "matches-list"})
            games = scope.find_all("div", attrs={"itemtype": "http://schema.org/SportsEvent"})
            dateFormat = "%m/%d/%Y"
            matches = []
            for game in games:
                match = []
                datePieces = game.find("meta", attrs= {"itemprop": "startDate","content": True}).attrs.get("content").split(" ")
                date = datePieces[0]
                date = datetime.datetime.strptime(date, dateFormat)
                date = str(datetime.date.strftime(date, outPutDateFormat))
                homeTeam = game.find("div", attrs={"class": "team-home is-club "}).text.strip()
                awayTeam = game.find("div", attrs={"class": "team-away is-club "}).text.strip()
                gameTime = game.find("span", attrs={"class": "js-tolocaltime match--score_time"}).text.strip()
                result = game.find("span", attrs={"class": "match--score_score"}).text.strip()
                match.append(homeTeam)
                match.append(awayTeam)
                match.append(result)
                match.append(date)
                match.append(gameTime)
                matches.append(match)
            schedule.append(matches)
            clURL = clURL[:-1]
            clURL =clURL + str(i + 5)
        return schedule

