#!/usr/bin/env python
# coding: utf-8

# In[5]:


import pandas as pd
import psycopg2
import pandas.io.sql as sqlio
import requests
import pickle
import config as cfg

class Data_Gathering:
    
    def __init__(self, df):
        self.df = df
        
    def get_table(self, sql_str):
        '''
        query the database and return a dataframe with given sql query string
        input: `sql_str`, query string
        return: a dataframe
        '''
        host= cfg.db['host']
        port = cfg.db['port']
        user = cfg.db['user']
        pwd = cfg.db['pwd']
        database= cfg.db['database']

        con = psycopg2.connect(database=database, user=user, password=pwd, host=host, port=port)

        print("Database opened successfully")

        sql = "'''" + sql_str + "'''"
        df = sqlio.read_sql_query(sql, con)

        return df
    
    def get_weather(self, df):
        '''
        request weather information
        input: a data frame in which
            - first column: date
            - second column: location in "latitude, longitude"        
        output: a dictionary 
        '''
        key = cfg.rapid_api['key']
        base_url = "https://dark-sky.p.rapidapi.com"
        headers = { 'x-rapidapi-host': "dark-sky.p.rapidapi.com",
                    'x-rapidapi-key': key }
        weather_dict = { 'weather':[] }

        count = 1
        for row in df.values:
            print('Query Count: ', count)
            date = row[0]
            ll = row[1]
            url = base_url + '/' + ll + ',' + date + 'T' + '13:00:00'        
            res = requests.get(url, headers=headers)
            if res.status_code == 200:
                weather_json = res.json()
                try:
                    weather = weather_json['currently']['summary']
                except:
                    weather = 'NA'
                finally:        
                    weather_dict['weather'].append(weather)
            else:
                weather_dict['weather'].append('NA')            
            count += 1
        return weather_dict


# In[2]:






