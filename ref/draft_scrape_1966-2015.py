"""
Scraping/cleaning data for drafts from 1966

"""
from urllib import urlopen
from bs4 import BeautifulSoup
import pandas as pd 

url_template = "http://www.basketball-reference.com/draft/NBA_{year}.html"

# empty DataFrate
draft_df = pd.DataFrame()

# for yr in range(1991, 1992):
for yr in range(1966, 2016):
	# get url
	url = url_template.format(year=yr)
	# get html
	html = urlopen(url)
	# BS object
	soup = BeautifulSoup(html, 'html.parser')
	# get column headers
	column_headers = [th.getText() for th in 
						soup.findAll('tr', limit=2)[1].findAll('th')]
	column_headers.pop(0)

	# get player data
	data_rows = soup.findAll('tr')[2:]
	player_data = [[td.getText() for td in data_rows[i].findAll('td')]
					for i in range(len(data_rows))]

	year_df = pd.DataFrame(player_data, columns=column_headers)
	year_df.insert(0,'Draft_Yr', yr)

	draft_df = draft_df.append(year_df, ignore_index=True)

# clean
draft_df = draft_df.convert_objects(convert_numeric=True)
draft_df = draft_df[draft_df.Player.notnull()]
draft_df = draft_df.fillna(0)
draft_df.rename(columns={'WS/48':'WS_per_48'}, inplace=True)
draft_df.columns = draft_df.columns.str.replace('%', '_pct')
draft_df.columns.values[15:19] = [draft_df.columns.values[15:19][col]
								+ "_per_G" for col in range(4)]
draft_df.loc[:,'Yrs':'AST'] = draft_df.loc[:,'Yrs':'AST'].astype(int)
draft_df.drop('Rk', axis='columns', inplace=True)
draft_df['Pk'] = draft_df['Pk'].astype(int)

draft_df.to_csv("draft_data_1966_to_2015.csv")
