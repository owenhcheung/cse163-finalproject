"""
takumi shimada, owen cheung, julia russell
cse 163 final project
this program processes the data
"""


# imports
import pandas as pd
import geopandas as gpd
import os


def rq1_processing(d1, d4, d6, shp_file):
    """
    this method merges datasets d1, d4, d5, and the us
    state shape file to create a new filtered dataset
    for research question 1
    """
    temp_change = pd.read_csv(d1)
    regions = pd.read_csv(d4)
    states = gpd.read_file(shp_file)
    # convert fips codes to int for merge
    states['STATEFP'] = states['STATEFP'].astype(int)
    # remove alaska (fips 2) + hawaii (fips 15)
    states = states[(states.STATEFP != 2) | (states.STATEFP != 15)]
    population = pd.read_csv(d6)
    # group by state -> get average % change in pop
    population = population.groupby(["Name"]).mean()
    # merge all the datasets together
    merged = states.merge(temp_change, left_on='STATEFP',
                          right_on='fips', how='left')
    merged2 = merged.merge(regions, left_on='STATE_NAME',
                           right_on='State', how='left')
    merged3 = merged2.merge(population, left_on='STATE_NAME',
                            right_on='Name', how='left')
    # filter out the columns that aren't needed + drop na values
    filtered_data = merged3[["fips", "State", "Annual", "Region",
                             "Percent Change in Resident Population",
                             "geometry"]]
    filtered_data = filtered_data.dropna()
    return filtered_data


def rq2_process(d1, d3):
    """
    this method merges datasets d1, and d3 to create a new
    filtered dataset for research question 2
    """
    merged = d1.merge(d3, left_on='STUSAB', right_on='usa_state_code',
                      how='left')
    mask = merged[['Annual', 'usa_state_code', 'usa_state_latitude',
                   'usa_state_longitude']]
    return mask


def ds1_process(path):
    """
    this method reads dataset d1 and returns it
    """
    return pd.read_csv(path)


def ds2_process():
    """
    description for this method
    """
    state_avg_dic = {'State': [], 'Average': []}
    directory = 'data/D2/'
    file_names = os.listdir(directory)
    for file_name in file_names:
        path = os.path.join(directory, file_name)
        df = pd.read_csv(path)
        df = df.dropna()
        state = path[8:-8]
        dfc = df.copy()
        if state == 'Delaware':
            dfc.loc[17, 'Unnamed: 1'] = 0
        new_wanted = dfc.loc[17, 'Unnamed: 1':'Unnamed: 5'] \
            .str.replace(',', '')
        new_wanted = new_wanted.dropna()
        new_wanted = new_wanted.astype(int)
        avg = new_wanted.sum() / 5
        state_avg_dic['State'].append(state)
        state_avg_dic['Average'].append(avg)
    return pd.DataFrame.from_dict(state_avg_dic)


def ds3_process(path):
    """
    this method reads dataset d3 and returns it
    """
    return pd.read_csv(path)


def ds4_process(path):
    """
    description for this method
    """
    df = pd.read_csv(path)
    return df.loc[:, ['State', 'Region']]
