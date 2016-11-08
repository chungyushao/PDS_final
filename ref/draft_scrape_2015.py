"""
Scraping and Cleaning the NBA Draft 

Use BeautifulSoup library to scrape data
Use pandas to store data scraped
"""
from urllib import urlopen
from bs4 import BeautifulSoup
import pandas as pd

url = "http://www.basketball-reference.com/draft/NBA_2015.html"
html = urlopen(url)

# BeautifulSoup object
url_bs = BeautifulSoup(html, "html5lib")

column_headers = [th.getText() for th in
				url_bs.findAll('tr', limit=2)[1].findAll('th')]

data_rows = url_bs.findAll('tr')[2:]

player_data = [[td.getText() for td in data_rows[i].findAll('td')]
			for i in range(len(data_rows))]

# create pandas DataFrame with column_headers and player_data
df = pd.DataFrame(player_data, columns=column_headers)

# get rid of rows with NaN values
df = df[df.Player.notnull()]

df.rename(columns={'WS/48':'WS_per_48'}, inplace=True)

df.columns = df.columns.str.replace('%','_pct')

df.columns.values[14:18] = [df.columns.values[14:18][col] +
								"_per_G" for col in range(4)]

df = df.convert_objects(convert_numeric=True)

# replace NaN values with 0s
df = df[:].fillna(0)

df.loc[:, 'Yrs' : 'AST'] = df.loc[:,'Yrs' : 'AST'].astype(int)

df.insert(0, 'Draft_Yr', 2014)
df.drop('Rk', axis='columns', inplace=True)

df.to_csv("draft_data_2014.csv")