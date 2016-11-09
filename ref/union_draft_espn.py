import pandas as pd 
from draft_scrape import scrape_draft
from ESPN_nba_player_stats import get_regular_season 

def union_draft_espn(draft_file, union_file, start_yr=1990, end_yr=2017):

	draft_df = pd.read_csv(draft_file, index_col=0)

	for yr in range(start_yr, end_yr):
		yr_data = get_regular_season(yr)
		# Only cares playes in draft_df
		draft_df = pd.merge(draft_df, yr_data, on="PLAYER", how="left")

	draft_df.to_csv(union_file)
	return draft_df

start_yr = 2009
end_yr = 2017 # exclusive

draft_file_format = "draft_data_{start_yr}_to_{end_yr}.csv"
union_file_format = "all_data_{start_yr}_to_{end_yr}.csv"
draft_file = draft_file_format.format(start_yr = start_yr, end_yr = end_yr)
union_file = union_file_format.format(start_yr = start_yr, end_yr = end_yr)

# Save all draft data
df = scrape_draft(draft_file, start_yr, end_yr)
union_draft_espn(draft_file, union_file, start_yr, end_yr)