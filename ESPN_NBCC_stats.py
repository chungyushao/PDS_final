from urllib import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def obj2numeric(df, cols, str_cols = ['Tm', 'Player', 'College']):
    """
    convert column type to numeric except those string fields
    
    Args:
    (data_frame): data frame to be converted
    
    Return:
    (data_frame): data frame with numeric fields converted
    """
    for c in cols:
        print df[c]
        if c not in str_cols: df[c] = pd.to_numeric(df[c], errors='raise')
    return df

def transform_numeric(df):
    """
    convert columns type to numeric
    
    Args:
    (data_frame): data frame whose columns contain object type
    
    Return:
    (data_frame): data frame with numeric values converted
    """
    df = obj2numeric(df, df.columns)
    return df

def scrape_draft(save_file, cur_url, past_url, start_yr=2002, end_yr=2018):
    """
    Scrape draft data for the specified duration from:
    http://www.basketball-reference.com/draft/NBA_{year}.html
    
    Args:
    start_yr(int): start of year for scraping
    end_yr(int): end of year for scraping
    
    Return:
    (data_frame): Annually draft pick result
    """
    frames = []
    
    for y in range(start_yr, end_yr):
        print "\t year = " + str(y)
        rows = []
        cols = []
        for cnt in range(0, 100, 40):
            if y == 2017:
                url = cur_url
            else:
                url = past_url.format(yr = y)

            if cnt > 0:
                url += "/count/" + str(cnt + 1)

            bs = BeautifulSoup(urlopen(url), 'html.parser')
            tr_tags = bs.findAll('tr')
            cur_rows = [[td.getText() for td in tr_tags[i].findAll('td')] for i in range(0, len(tr_tags))]
            cols = cur_rows[0]

            pop_num = int(len(cur_rows) / 11)
            while pop_num > 0:
                cur_rows.pop((pop_num - 1) * 11)
                pop_num -= 1
            rows += cur_rows

        cur_df = pd.DataFrame(rows, columns = cols)
        # RK columns may be empty string
        cur_df.drop('RK', axis=1, inplace=True)
        cur_df['RK'] = list(range(1, len(cur_df) + 1))
        cur_df['Year'] = y
        frames.append(cur_df)
    
    df = pd.concat(frames)
    df.to_csv(save_file)
    return df

# start_yr stands for {start_yr}-{start_yr + 1} Regular Season
start_yr=2016
end_yr=2018 # exclusive
file_format = "{category}_{start_yr}_to_{end_yr}.csv"
categories = ['scoring', 'rebounds', 'assits', 'steals', 'blocks']
cur_urls = ['scoring-per-game/sort/avgPoints', 'rebounds/sort/avgRebounds', 'assists', 'steals/sort/avgSteals', 'blocks']
past_urls = ['scoring-per-game/sort/avgPoints/year/{yr}', 'rebounds/year/{yr}', 'assists/sort/avgAssists/year/{yr}', 'steals/year/{yr}', 'blocks/sort/avgBlocks/year/{yr}']
for category, cur_url, past_url in zip(categories, cur_urls, past_urls):
    print "processing : " + category
    base_url = 'http://www.espn.com/mens-college-basketball/statistics/player/_/stat/'
    file_name = file_format.format(category = category, start_yr = start_yr, end_yr = end_yr)
    scrape_draft(file_name, base_url + cur_url, base_url + past_url, start_yr, end_yr)