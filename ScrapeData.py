from scrapeCollection import ScheduleCollection
import sqlite3

conn = sqlite3.connect("leagueSchedule.db")
c = conn.cursor()


def create_prem_schedule():
    premierLeagueData = ScheduleCollection().premScrape()
    c.execute('CREATE TABLE IF NOT EXISTS PremierLeague(Home TEXT, Away TEXT, ResultTime TEXT, date TEXT)')
    conn.commit()
    for element in premierLeagueData:
        homeTeam = element[0]
        awayTeam = element[1]
        resultORTime = element[2]
        date = element[3]
        c.execute("INSERT INTO PremierLeague VALUES (?, ?, ?, ?)", (homeTeam, awayTeam, resultORTime, date))
        conn.commit()
    c.execute("SELECT * FROM PremierLeague")
    print(c.fetchall())
    c.close()


def create_bundesliga_schedule():
    bundesligaData = ScheduleCollection().bundScrape()
    c.execute('CREATE TABLE IF NOT EXISTS Bundesliga(Home TEXT, Away TEXT, Result TEXT, date TEXT, time TEXT)')
    conn.commit()
    for matchweek in bundesligaData:
        for game in matchweek:
            homeTeam = game[0]
            awayTeam = game[1]
            result = game[2]
            date = game[3]
            time = game[4]
            c.execute("INSERT INTO Bundesliga VALUES (?, ?, ?, ?, ?)", (homeTeam, awayTeam, result, date, time))
            conn.commit()
    c.execute("SELECT * FROM Bundesliga")
    print(c.fetchall())
    c.close()


def create_calcio_schedule():
    calcioAData = ScheduleCollection().calcioScrape()
    c.execute('CREATE TABLE IF NOT EXISTS CalcioA(Home TEXT, Away TEXT, Result TEXT, date TEXT, time TEXT)')
    conn.commit()
    for matchweek in calcioAData:
        for game in matchweek:
            homeTeam = game[0]
            print(homeTeam)
            awayTeam = game[1]
            result = game[2]
            date = game[3]
            time = game[4]
            c.execute("INSERT INTO CalcioA VALUES (?, ?, ?, ?, ?)", (homeTeam, awayTeam, result, date, time))
            conn.commit()
    c.execute("SELECT * FROM CalcioA")
    print(c.fetchall())
    c.close()


def create_ligue1_schedule():
    ligue1Data = ScheduleCollection().ligueScrape()
    c.execute('CREATE TABLE IF NOT EXISTS Ligue1(Home TEXT, Away TEXT, Result TEXT, date TEXT, time TEXT)')
    conn.commit()
    for matchweek in ligue1Data:
        for game in matchweek:
            homeTeam = game[0]
            awayTeam = game[1]
            result = game[2]
            date = game[4]
            time = game[3]
            c.execute("INSERT INTO Ligue1 VALUES (?, ?, ?, ?, ?)", (homeTeam, awayTeam, result, date, time))
            conn.commit()
    c.execute("SELECT * FROM Ligue1")
    print(c.fetchall())
    c.close()


def create_cl_groupstage():
    clgroupstageData = ScheduleCollection().championsleaguegroupgames()
    c.execute('CREATE TABLE IF NOT EXISTS ChampionsLeagueGroupStage'
              '(Home TEXT, Away TEXT, Result TEXT, date TEXT, time TEXT)')
    conn.commit()
    for matchweek in clgroupstageData:
        for game in matchweek:
            homeTeam = game[0]
            awayTeam = game[1]
            result = game[2]
            date = game[3]
            time = game[4]
            c.execute("INSERT INTO ChampionsLeagueGroupStage VALUES (?, ?, ?, ?, ?)",
                      (homeTeam, awayTeam, result, date, time))
            conn.commit()
    c.execute("SELECT * FROM ChampionsLeagueGroupStage")
    print(c.fetchall())
    c.close()


# create_cl_groupstage()


# c.execute("DELETE FROM PremierLeague")
# c.execute("DELETE FROM Bundesliga")
# c.execute("DELETE FROM CalcioA")
# c.execute("DELETE FROM PremierLeague")
