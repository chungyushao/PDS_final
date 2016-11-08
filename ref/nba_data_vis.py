import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns

draft_df = pd.read_csv('draft_data_1966_to_2015.csv', index_col=0)
"""
Plot give data for each year on graph
input: title, y_label, y_values, y_llim, y_ulim, source_space

output: a pretty graph (hopefully)
"""
def plot_graph(title,y_label,y_values,y_llim,y_ulim,source_space):
	# get x-axis (years)
	x_values = draft_df.Draft_Yr.unique()
	# make graph
	sns.set_style("white") # set graph style to white
	plt.figure(figsize=(12,9)) # width = 12", height = 9"
	plt.title(title,fontsize=20) # readability
	plt.ylabel(y_label, fontsize=18)
	plt.xlim(1966,2015.5) # setting x-axis and y-axis lim to where data is
	plt.ylim(y_llim,y_ulim)
	plt.grid(axis='y', color='grey', linestyle='--', lw=0.5, alpha=0.5)
	plt.tick_params(axis='both', labelsize=14) # readability
	sns.despine(left=True, bottom=True) # get rid of borders
	plt.plot(x_values, y_values)
	plt.text(1966, source_space, \
			'Primary Data Source: http://www.basketball-reference.com/draft/'
			'\nAuthor: Noman Siddiqui (nomansid.github.io)', \
			fontsize=12)
	plt.show

# plot ws/48 data
plot_graph('Average Career Win Shares Per 48 minutes by Draft Year (1966-2015)',
			'Win Shares Per 48 minutes', draft_df.groupby('Draft_Yr').WS_per_48.mean(),
			0, 0.08, -0.009) 
plt.savefig("ws48_by_draft_year.png")
plt.clf()