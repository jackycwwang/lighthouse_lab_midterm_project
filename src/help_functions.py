import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import requests
from sklearn.preprocessing import StandardScaler
import config as cfg

def split_numeric_categorical(df, numeric=True):
    '''    
    Return either numerical columns, or categorical columns in a data frame
    numeric: default True, return dataframe of all numerical columns    
    input: a data frame
    output: a data frame    
    '''
    numeric_data = df.select_dtypes(include=[np.number])
    categorical_data = df.select_dtypes(include='category')
    if numeric:
        return numeric_data
    else:
        return categorical_data


def make_categorical(df, cols):
    '''
    Convert columns in `cols` to type `categorical`
    input: df - data frame, cols - a list of columns
    output: a copy of the data frame with the converted columns
    '''
    col_dict = {col:'category' for col in cols}
    df = df.astype(col_dict)
    return df


def to_hhmmss(df_time_col):
    '''
    Change the format of the time in hhmm
    to hh:mm:ss, where ss is 00 in this case
    Input: `df_time_col`: a Pandas Series
    Return: a Pandas Series
    '''
    
    hhmm = []
    crs_hm = df_time_col.astype('str')
    for t in crs_hm:
        if len(t) == 1:
            hhmm.append('0' + t + ':00:00')
        elif (len(t) == 2) & (t < '24'):
            hhmm.append(t + ':00:00')
        elif (len(t) == 2) & (t > '24'):
            hhmm.append('00:' + t + ':00')
        elif len(t) == 3:
            hhmm.append('0' + t[0] + ':' + t[1:] + ':00')
        else:
            hhmm.append(t[:2] + ':' + t[2:] + ":00")
    return hhmm




def to_city_state(city_state_col):
    '''
    Change the format of `city1/city2, state`
    to `city1, state` 
    Input: A Pandas Series
    Output: A Pandas Series
    '''
    return pd.Series(map(lambda x: x[0].split('/')[0] + ',' + x[-1].strip() ,
                    city_state_col.str.split(',')))



def to_hhmmss(df_time_col):
    '''
    Change the format of the time in hhmm
    to hh:mm:ss, where ss is 00 in this case
    Input: `df_time_col`: a Pandas Series
    Return: a Pandas Series
    '''
    
    hhmm = []
    crs_hm = df_time_col.astype('str')
    for t in crs_hm:
        if len(t) == 1:
            hhmm.append('0' + t + ':00:00')
        elif (len(t) == 2) & (t < '24'):
            hhmm.append(t + ':00:00')
        elif (len(t) == 2) & (t > '24'):
            hhmm.append('00:' + t + ':00')
        elif len(t) == 3:
            hhmm.append('0' + t[0] + ':' + t[1:] + ':00')
        else:
            hhmm.append(t[:2] + ':' + t[2:] + ":00")
    return hhmm



def merge_df_dict(df_time_ll, dic):
    '''
    Make a new dataframe with weather column,
    then merge the new dataframe with original dataframe
    input: df_time_ll, the dataframe where the `dic` is going to be concatenated on
    return: The joined version of original dataframe
    '''
    df_time_ll = pd.concat([df_time_ll, pd.DataFrame.from_dict(dic)], axis=1)
    df = df.merge(df_time_ll, on=['fl_date', 'll'], how='left')
    return df


def to_dummies(df, col_array):
    '''
    change the given columns into dummy variables
    and return the dataframe
    '''
    return pd.get_dummies(df, columns= col_array, drop_first=True)




def to_scale(df, col_array):
    '''
    scale the numeric variables to center around 0
    and standard deviation of 1
    '''
    sc = StandardScaler()
    df[col_array] = pd.DataFrame(sc.fit_transform(df[col_array]))   




def inverse_scale(df, col_array, sc):    
    '''
    inverse scale back to the original numeric values
    '''
    df[col_array] = pd.DataFrame(sc.inverse_transform(df[col_array]))




