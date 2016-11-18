# -*- coding: utf-8 -*-

from urllib import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

bs = BeautifulSoup(urlopen("http://www.nba-allstar.com/players/"), 'html.parser')
validPattern = r"\w*[\'-]*\w*\s+\w*[\'-]*\w*"
playerlist = []

for res in bs.find_all('a'):
    if res.text:
        text = res.text.strip()
        if re.match(validPattern, text):
            text = re.sub(r"\s+", " ", text)
            print text
            playerlist += [text]
            #playerlist.append(re.match())

f = open('all_star_list.csv', 'w')
f.write("PLAYER\n")
for name in playerlist[12:-2]:
    f.write(name + "\n")
f.close()
