# -*- coding: utf-8 -*-
"""

Modified from Reference

1) Rename columns of yr_data, extending year information
2) Extend functions to crawl past data
3) Fix bugs where page counts are less than list s

Reference: Github repository of Zhongxiang Dai

"""

import re
import requests
import pandas as pd
import numpy as np


def get_row(source):
    h_code = re.compile(u'<td.*?>.*?</td>', re.S)
    all_ele = re.findall(h_code, source)
    all_e = []
    for ele in all_ele:
        ele = re.sub(u'<.*?>', '', ele)
        all_e.append(ele)
    return all_e
def get_all_player(rows):
    all_player = []
    for row in rows:
        all_player.append(get_row(row))
    return all_player

# Extract the table of stats and return them in rows
def get_all_rows(url):
    req = requests.get(url).text
    table_code = re.compile(u'<table.+>(.+?)</table>', re.S) # re.S for ignoring newline char
    table = re.search(table_code, req) # Find the table on the current page
    table = table.group(0)
    row_code = re.compile(u'<tr.+?>.+?</tr>', re.S)
    return re.findall(row_code, table) # Find and return all rows

# Get all stats on a page
def get_data(url):
    # print url
    rows = get_all_rows(url)
    all_player = get_all_player(rows)
    all_player = pd.DataFrame(all_player) # Convert that stats to Pandas DataFrame
    # Empty results
    if (all_player.shape[0] == 0):
        return all_player
    # Drop the index rows inside the table
    all_player = all_player.drop([0], axis=1)
    ind = all_player.loc[:,1] != 'PLAYER'
    ind[0] = True
    all_player = all_player[ind]
    return all_player

def get_all_data(url, s_str):
    all_data = []
    for s in s_str:
        url1 = url + s
        cur_data = get_data(url1)
        if cur_data.shape[0] != 0:
            all_data.append(cur_data)
    all_data = pd.concat(all_data)
    all_data.index = np.arange(all_data.shape[0])
    # Drop the index rows inside the table
    ind = all_data.loc[:,1] != 'PLAYER'
    ind[0] = True
    all_data = all_data[ind]
    all_data.index = np.arange(all_data.shape[0])
    return all_data

# Get all data of one specified regular season starting from yr to yr + 1
def get_regular_season(start_yr=2016):
    cur_yr = 2016
    base_url = 'http://espn.go.com/nba/statistics/player/_/stat/'
    url_pts = base_url + 'scoring-per-game/sort/avgPoints/' # average points leader board
    url_reb = base_url + 'rebounds/sort/avgRebounds/' # average rebound leader board
    url_ass = base_url + 'assists/sort/avgAssists/' # average assists leader board

    # Modify urls if yr is not equal to 2016
    if start_yr != cur_yr: 
        url_pts += "year/" + str(start_yr) + "/"

    # Get url increment rules
    s = np.arange(41, 300, 40)
    s_str = ['']
    for i in s:
        s_str.append('count/' + str(i))

    yr_data = get_all_data(url_pts, s_str)

    # Extract player position
    yr_pos = []
    pos_code = re.compile(u',.+')
    for n in yr_data.loc[1:,1]:
        p = re.search(pos_code, n).group(0)
        yr_pos.append(re.sub(u', ', '', p))

    pos = ["POS"] + yr_pos
    yr_data.insert(1, "POS", pos)

    # Clean the column of player name
    si = yr_data.shape[0]
    for i in range(si - 1):
        yr_data.loc[i + 1, 1] = re.sub(u',.*', '', yr_data.loc[i + 1, 1])

    # Rename all columns, and remove row 1 
    pre_str = str(start_yr) + "_"
    keys = [col for col in yr_data.columns]
    values = ["PLAYER"] + [pre_str + str(col) for col in yr_data.loc[0, :][1:].tolist()]
    yr_data.rename(columns=dict(zip(keys,values)), inplace=True)
    yr_data.drop(0, inplace=True)

    return yr_data