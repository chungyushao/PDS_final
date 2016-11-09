from urllib import urlopen
from bs4 import BeautifulSoup
import pandas as pd

def obj2numeric(df, cols, str_cols = ['Tm', 'PLAYER', 'College']):
    """
    convert column type to numeric except those string fields
    
    Args:
    (data_frame): data frame to be converted
    
    Return:
    (data_frame): data frame with numeric fields converted
    """
    for c in cols:
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
    df.rename(columns={'WS/48':'WS_per_48', 'Player':'PLAYER'}, inplace=True)
    df.columns.values[14:18] = [df.columns.values[14:18][col] + "_per_game" for col in range(4)]
    df = obj2numeric(df, df.columns)
    df = df[df['PLAYER'].notnull()].fillna(0)
    df.loc[:,'Yrs':'AST'] = df.loc[:,'Yrs':'AST'].astype(int)
    return df
    
def scrape_draft(save_file, start_yr=1966, end_yr=2016):
    """
    Scrape draft data for the specified duration from:
    http://www.basketball-reference.com/draft/NBA_{year}.html
    
    Args:
    start_yr(int): start of year for scraping
    end_yr(int): end of year for scraping
    
    Return:
    (data_frame): Annually draft pick result
    """
    url_format = 'http://www.basketball-reference.com/draft/NBA_{yr}.html'
    frames = []
    
    for y in range(start_yr, end_yr):
        url = url_format.format(yr = y)
        bs = BeautifulSoup(urlopen(url), 'html.parser')
        
        # columns and remove the header column(Rk)
        tr_tags = bs.findAll('tr')
        th_tags = tr_tags[1].findAll('th')
        
        cols = [th.getText() for th in th_tags]; cols.pop(0)
        rows = [[td.getText() for td in tr_tags[i].findAll('td')] for i in range(2, len(tr_tags))]

        year_df = pd.DataFrame(rows, columns = cols)
        year_df.insert(0,'Draft_Yr', y)
        frames.append(year_df)
    
    df = pd.concat(frames)
    df = transform_numeric(df)
    df.to_csv(save_file)
    return df