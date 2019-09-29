import pandas
import sqlite3
import os
import csv

conn = sqlite3.connect("footballData.db")
c = conn.cursor()

premMasterFolder = "/Users/Tilley/Desktop/footballcsv/premcsv/eng-england-master/"
spainMasterFolder = "/Users/Tilley/Desktop/footballcsv/spaincsv/es-espana-master"
gerMasterFolder = "/Users/Tilley/Desktop/footballcsv/gercsv/de-deutschland-master"
franceMasterFolder = "/Users/Tilley/Desktop/footballcsv/francecsv/fr-france-master"
italyMasterFolder = "/Users/Tilley/Desktop/footballcsv/italycsv/it-italy-master"
mexMasterFolder = "/Users/Tilley/Desktop/footballcsv/mexicocsv/mx-mexico-master"
nedMasterFolder = "/Users/Tilley/Desktop/footballcsv/nedcsv/nl-netherlands-master"
porMasterFolder = "/Users/Tilley/Desktop/footballcsv/porcsv/pt-portugal-master"
champsMasterFolder = "/Users/Tilley/Desktop/footballcsv/champscsv/europe-champions-league-master"
mlsMasterFolder = "/Users/Tilley/Desktop/footballcsv/mlscsv/major-league-soccer-master"


def make_games_table(dire,league):
    for root, dirs, files in os.walk(dire):
        for name in files:
            if name.startswith("1-"):
                csv_title = root + "/" + name
                # season_id = root[-7:-3]
                season_id = (root[-4:]) #mls

                add_seasonid_csv(csv_title, season_id)
                add_leagueid_csv(csv_title, league)

                df = pandas.read_csv(csv_title)
                df.to_sql("Cup_games", conn, if_exists='append', index=False)



def add_seasonid_csv(csvfile,season_id):
    csv_input = pandas.read_csv(csvfile)
    csv_input['Season_id'] = season_id
    csv_input.to_csv(csvfile, index=False)


def add_leagueid_csv(csvfile,league_id):
    csv_input = pandas.read_csv(csvfile)
    csv_input['League_id'] = league_id
    csv_input.to_csv(csvfile, index=False)

def todb(csv_title,table):
    df = pandas.read_csv(csv_title)
    df.to_sql(table, conn, if_exists='append', index=False)

# make_games_table(premMasterFolder, league="1")
# make_games_table(spainMasterFolder, league="2")
# make_games_table(gerMasterFolder, league="3")
# make_games_table(franceMasterFolder, league="4")
# make_games_table(italyMasterFolder, league="5")
# make_games_table(porMasterFolder, league="6")
# make_games_table(nedMasterFolder, league="7")
# make_games_table(mexMasterFolder, league="8")
# make_games_table(champsMasterFolder, league="9")
# make_games_table(mlsMasterFolder, league=10)

todb("PlayerTransferHistory.csv","PlayerTransferHistory")