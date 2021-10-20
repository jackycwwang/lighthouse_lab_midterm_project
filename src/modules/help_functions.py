import numpy as np
import pandas as pd

delay_col_list= ['carrier_delay', 
                 'weather_delay', 
                 'nas_delay', 
                 'security_delay', 
                 'late_aircraft_delay' 
                 ]

top20_airport_code = ['LAX', 'ORD', 'EWR', 'SFO', 'LGA', 'DFW', 'LAS', 'CLT', 'DEN',
                      'PHL', 'IAH', 'SEA', 'ATL', 'PHX', 'MCO', 'DTW', 'SLC', 'BOS',
                      'JFK', 'MSP']

cat_cols = ['mkt_unique_carrier', 'branded_code_share', 'mkt_carrier', 
            'op_unique_carrier', 'origin_airport_id', 'origin', 
            'origin_city_name', 'dest_airport_id', 'dest', 
            'dest_city_name', 'cancelled', 'cancellation_code']


cols_to_drop = ['origin_airport_fl_amt_bin', 
                'dest_airport_fl_amt_bin', 
                'dest_0', 
                'weekday_0', 'weekday_1', 'weekday_2', 'weekday_3', 'weekday_4', 
                'weekday_5', 'weekday_6', 
                'origin_city_0', 
                'origin_state_0']    

states_to_drop = [
 'origin_state_CA',
 'origin_state_CO',
 'origin_state_FL',
 'origin_state_GA',
 'origin_state_IL',
 'origin_state_NC',
 'origin_state_NY',
 'origin_state_PA',
 'origin_state_TX',
 'origin_state_WA', 
 'dest_state_CA',
 'dest_state_CO',
 'dest_state_FL',
 'dest_state_GA',
 'dest_state_IL',
 'dest_state_NC',
 'dest_state_NY',
 'dest_state_PA',
 'dest_state_TX',
 'dest_state_WA',]


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


def make_bin_column(df, col_name, n_bin_range):
    '''
    Convert a numeric column to a categorical ordinal column.
    Assumption: the column that is going to be binned
    must be positive numeric numbers
    input:
      - df: data frame
      - col_name: column in string
      - n_bin_range: number of bin required
    return: a data frame with the newly binned column  
    '''
    # make bins and bin labels
    bin_names = range(1, n_bin_range+1)
    
    # perform the binning
    new_col_name = col_name + '_bin'
    df[new_col_name] = pd.cut(np.array(df[col_name]), 
                              bins=n_bin_range, 
                              labels=bin_names)
    return df

def make_qbin_column(df, col_name, n_bin_range):
    '''
    Convert a numeric column to a ordinal column based on quantiles.
    Assumption: the column that is going to be binned
    must be positive numeric numbers
    input:
      - df: data frame
      - col_name: column in string
      - q_list: a list of quantiles to be binned, 
        eg., [0, 0.25, 0.50, 0.75, 1] for 4-quantiles
    return: a data frame with the newly binned column  
    '''
    # make bin labels
    if type(n_bin_range) is list:
        bin_names = list(range(1, len(n_bin_range)+1))
    elif type(n_bin_range) is int:
        bin_names = range(1, n_bin_range+1)
    
    # perform the binning
    new_col_name = col_name + '_bin'
    df[new_col_name] = pd.qcut(np.array(df[col_name]), 
                               q=n_bin_range, 
                               labels=bin_names, 
                               duplicates='drop')
    return df

def split_time_of_day_departure(df):
    """ takes estimated time of departure and splits in to hours 24 hour clock (local time) """
    df['dep_hour'] = df['crs_dep_time']
    df['dep_hour'] = np.floor(df['dep_hour']/100).astype("int")
    return df
  
    
def split_time_of_day_arrival(df):
    """ takes estimated time of arrival and splits in to hours 24 hour clock (local time) """
    df['arr_hour'] = df['crs_arr_time']
    df['arr_hour'] = np.floor(df['arr_hour']/100).astype("int")
    return df
    
    
def split_dest_city_state(df):
    """ separates destination city and states into own columns"""
    df['dest_state'] = df['dest_city_name']
    df['dest_city'] = df['dest_city_name']
    
    f_state= lambda x: x.split(sep=', ')[1]
    f_city= lambda x: x.split(sep=', ')[0]

    df['dest_state'] = df['dest_state'].apply(f_state)
    df['dest_city'] = df['dest_city'].apply(f_city)
    return df

def create_haul_type(self):
    """ adds short:0, mid:1, long:2 range haul types from crs_elapsed_time (scheduled) """

    self.df["haul_type"] = self.df['crs_elapsed_time']
    self.df["haul_type"].mask(self.df["haul_type"].values < 180, 0, inplace=True)
    self.df["haul_type"].mask((self.df["haul_type"] >= 180) & (self.df["haul_type"] < 360), 1, inplace=True)
    self.df["haul_type"].mask((self.df["haul_type"] >= 360), 2, inplace=True) 
    df["haul_type"]= df["haul_type"].astype('int')
    return self.df

def split_origin_city_state(df):
    """ separates origin city and states into own columns"""
    df['origin_state'] = df['origin_city_name']
    df['origin_city'] = df['origin_city_name']
    
    f_state= lambda x: x.split(sep=', ')[1]
    f_city= lambda x: x.split(sep=', ')[0]

    df['origin_state'] = df['origin_state'].apply(f_state)
    df['origin_city'] = df['origin_city'].apply(f_city)
    return df

def encode_and_bind(original_dataframe, feature_to_encode):
    dummies = pd.get_dummies(original_dataframe[[feature_to_encode]], drop_first=True)
    res = pd.concat([original_dataframe, dummies], axis=1)
#     res = res.drop([feature_to_encode], axis=1)
    return(res)

def add_weekday(df):
    """ creates boolean column to indicate day of week 
        https://pandas.pydata.org/docs/reference/api/pandas.DatetimeIndex.weekday.html
        week starts 0 with monday) """

    df['weekday'] = pd.to_datetime(df['fl_date'])
    f = lambda x: str(x.weekday())  
    df['weekday'] = df['weekday'].apply(f)
    return df

def make_col_value_bins(df, col_name, new_col_bin_name, n_bin_range):
    type_count = df[col_name].value_counts()
    df1 = pd.DataFrame(type_count).reset_index()
    df1 = df1.rename(columns={'index': col_name, col_name: 'count'})
    df1 = make_bin_column(df1, 'count', n_bin_range)
    df = df.merge(df1, on=col_name, how='left')
    df = df.rename(columns ={'count_bin': new_col_bin_name})
    df.drop(columns=['count', col_name], inplace=True)
    return df


def make_col_value_qbins(df, col_name, new_col_bin_name, n_bin_range, drop=True):
    type_count = df[col_name].value_counts()
    df1 = pd.DataFrame(type_count).reset_index()
    df1 = df1.rename(columns={'index': 'bin_on', col_name: 'count'})       
    df1 = make_qbin_column(df1, 'count', n_bin_range)
    df = df.merge(df1, left_on=col_name, right_on='bin_on', how='left')
    df = df.rename(columns ={'count_bin': new_col_bin_name})
    df.drop(columns=['count', col_name], inplace=True)
    if drop:
        df.drop(columns='bin_on', inplace=True) 
    return df

def get_avg_dest_delay(df, col_list):
    df.loc[:, col_list] = df.loc[:, col_list].fillna(0)
    df_avg_delay = pd.DataFrame(df.dest.unique(), columns=['dest'])
    for col in col_list:
        s = df.groupby('dest')[col].mean()
        s.name = 'avg_' + col
        df_avg_delay = df_avg_delay.merge(s.to_frame(), on='dest', how='left')
    return df_avg_delay

def get_avg_dep_delay(df, col_list):
    df.loc[:, col_list] = df.loc[:, col_list].fillna(0)
    df_avg_delay = pd.DataFrame(df.dest.unique(), columns=['origin'])
    for col in col_list:
        s = df.groupby('origin')[col].mean()
        s.name = 'avg_' + col
        df_avg_delay = df_avg_delay.merge(s.to_frame(), on='origin', how='left')
    return df_avg_delay