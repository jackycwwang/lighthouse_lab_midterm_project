import help_functions as hf
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMAxScaler


# df = pd.read_csv('../data/flights_samp.csv')

def convert_testtrain_data_to_test_format(df):
    """ Convert our testing data to be in the same format as the data to test (drop columns and reformat date)"""
    
    #convert date to datetime with 0's
    df.fl_date = (df.fl_date + ' 00:00:00')
    pd.to_datetime(df['fl_date'])
    
    #drop columns not present in test format
    df.drop(columns=['index', 'dep_time',
       'dep_delay', 'taxi_out', 'wheels_off', 'wheels_on', 'taxi_in', 'arr_time', 'arr_delay', 'cancelled',
       'cancellation_code', 'diverted', 'actual_elapsed_time', 'air_time', 
       'carrier_delay', 'weather_delay', 'nas_delay', 'security_delay',
       'late_aircraft_delay', 'first_dep_time', 'total_add_gtime',
       'longest_add_gtime', 'no_name'], inplace = True)
    return df
# df_new = convert_testtrain_data_to_test_format(df)


# THIS WILL BE CHANGED AS WE FEATURE ENGINEER

def convert_from_test_format_to_fit_predict_format(df):
    """Adds in columns for model fitting and converts to numeric/ encoded categorical for ML model"""
    
    # Split crs_arr_time and crs_dep_time into hour of day (local)
    df = hf.split_time_of_day_departure(df)
    df = hf.split_time_of_day_arrival(df)
    df.drop(columns=['crs_dep_time', 'crs_arr_time'], inplace=True)
    
    # Convert fl_date into day of week  # NOTE MAY WANT TO ADD BACK IN MONTH OR JAN 1 days
    df = hf.add_weekday(df)  
    df.drop(columns=['fl_date'], inplace=True)
    df.weekday = df.weekday.astype(str)
    df = hf.encode_and_bind(df, 'weekday')
    
    # Split city and state 
    hf.split_origin_city_state(df)
    hf.split_dest_city_state(df)
    df.drop(columns=['dest_city_name', 'origin_city_name'], inplace=True)
    
    # City - Encode (based on # flights)
    city_dict = {'Chicago': 10,
             'Atlanta': 9,
             'New York': 8,
             'Dallas/Fort Worth': 7,
             'Denver': 6,
             'Charlotte': 5,
             'Houston': 4,
             'Washington': 3,
             'Los Angeles': 2,
             'Seattle': 1}
    df = df.replace({"dest_city":city_dict})
    df = df.replace({"origin_city":city_dict})
    
    city_list = [10,9,8,7,6,5,4,3,2,1]
    df.dest_city = np.where(df.dest_city.isin(city_list),df.dest_city, 0)
    df.origin_city = np.where(df.origin_city.isin(city_list),df.origin_city, 0)
    
    # State - Encode (based on # flights)
    state_dict = {'CA': 10,
                 'TX': 9,
                 'FL': 8,
                 'IL': 7,
                 'NY': 6,
                 'GA': 5,
                 'NC': 4,
                 'CO': 3,
                 'PA': 2,
                 'WA': 1}

    df = df.replace({"dest_state":state_dict})
    df = df.replace({"origin_state":state_dict})
    
    state_list = [10,9,8,7,6,5,4,3,2,1]
    df.dest_state = np.where(df.dest_state.isin(state_list),df.dest_state, 0)
    df.origin_state = np.where(df.origin_state.isin(state_list),df.origin_state, 0)
          
    # Convert Carrier - Encode 
    df = hf.encode_and_bind(df, 'mkt_unique_carrier')
    df.drop(columns = ['mkt_unique_carrier'], inplace=True)

    # Origin Airport - Encode top 10 (rest in 'other') OR BIN according to passenger or flight volume
    df = hf.make_col_value_bins(df, 'origin', 'origin_airport_fl_amt_bin', 7) 
    
    # Dest Airport - Encode top 10 or bin according to passenger of flight volume 
    df = hf.make_col_value_bins(df, 'dest', 'dest_airport_fl_amt_bin', 7) 
   
    # Flight number ??? # drop for now? - See if routes that have more delays? Bin when find relationship with delays
    df.drop(columns = ['mkt_carrier_fl_num'], inplace=True)
    
    # Drop rest
    df.drop(columns=['branded_code_share', 'mkt_carrier','op_unique_carrier', 'tail_num', 
                     'op_carrier_fl_num', 'origin_airport_id', 'dest_airport_id', 'dup', 'flights'], inplace = True)
    
    # crs_elapsed # USE LONG HAUL SHORT HAUL
    df['log_crs_elapsed_time'] = np.log(df.crs_elapsed_time)
    df = hf.make_bin_column(df, 'log_crs_elapsed_time', 20) # 8-2/0.3
    df.drop(columns = ['crs_elapsed_time'], inplace=True)
    
    return df

    #/ distance choose one or other - correlated removal?

# df_new = convert_from_test_format_to_fit_predict_format(df_new)    





def load_preprocessed_data():
    """ read in data file, convert to the format the given test data is in and add / format columns per feature engineering """
    df = pd.read_csv('../data/flights_samp.csv')
    df = convert_testtrain_data_to_test_format(df)
    df = convert_from_test_format_to_fit_predict_format(df)
    return df


def process_data(df):
    df = remove_highly_correlated_features(df, correlation_threshold=0.8)
    df = remove_small_variance(x, variance_threshold = 0.1)
#     SCALE DATA

def remove_highly_correlated_features(df, correlation_threshold=0.8):
    #     Anything above correlation threshold will be tossed
    # Assumptions - all numeric, target variable removed
    # step 1
    df_corr = df.corr().abs()

    # step 2
    indices = np.where(df_corr > correlation_threshold)
    indices = [(df_corr.index[x], df_corr.columns[y])
    for x, y in zip(*indices)
        if x != y and x < y]

    # step 3
    for idx in indices: #each pair
        try:
            df.drop(idx[1], axis = 1, inplace=True)
        except KeyError:
            pass
    return(df)

 
def remove_small_variance(x, variance_threshold = 0.1):
    # Assumptions - target variable removed, df is numeric
    # import:
    # from sklearn.feature_selection import VarianceThreshold
    vt = VarianceThreshold(variance_threshold)
    x_transformed = vt.fit_transform(x)
    selected_columns = x.columns[vt.get_support()]
    x_transformed = pd.DataFrame(x_transformed, columns = selected_columns)
    return(x_transformed)

def remove_missing_values(x, missing_percent_drop_threshold=0.5):
#     takes in dataframe, removes missing above a percent threshold - percent out of 1
    total = x.isnull().sum().sort_values(ascending=False)
    percent = (x.isnull().sum()/x.isnull().count()).sort_values(ascending=False)
    missing_data = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
    missing_data.head(20)

    to_drop = missing_data[missing_data['Percent'] > missing_percent_drop_threshold].index.tolist()
    return(x.drop(to_drop, axis=1, inplace=True))

