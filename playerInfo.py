import csv
import pandas as pd
import re
from datetime import datetime

def removedup(csvin,csvout):
    infile = open(csvin, 'r')
    outfile = open(csvout, 'w')
    listlines = []
    for line in infile:
        if line in listlines:
            continue
        else:
            outfile.write(line)
            listlines.append(line)
    outfile.close()
    infile.close()

def removenumbers(csvin,csvout):
    infile = open(csvin, 'r')
    outfile = open(csvout, 'w')
    pattern = re.compile("^[0-9]+[0-9]?")
    for line in infile:
        x = pattern.match(line)
        if x is not None:
            x = re.sub(pattern,"",line)
            outfile.write(x)
        else:
            outfile.write(line)


def sortbydate(csvin,csvout):
    data = csv.reader(open(csvin, 'r'))
    data = sorted(data, key=lambda row: datetime.strptime(row[2], "%d/%m/%Y"))
    print(data)


#sortbydate("playersInfo.csv","")
#removedup('players.csv', 'playersInfo.csv')
#removenumbers('playersInfo.csv', 'playerData.csv')