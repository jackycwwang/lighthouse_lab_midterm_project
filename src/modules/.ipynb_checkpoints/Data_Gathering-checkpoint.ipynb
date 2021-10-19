{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "0e973739",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import psycopg2\n",
    "import pandas.io.sql as sqlio\n",
    "import requests\n",
    "import pickle\n",
    "import config as cfg\n",
    "\n",
    "class Data_Gathering:\n",
    "    \n",
    "    def __init__(self, df):\n",
    "        self.df = df\n",
    "        \n",
    "    def get_table(self, sql_str):\n",
    "        '''\n",
    "        query the database and return a dataframe with given sql query string\n",
    "        input: `sql_str`, query string\n",
    "        return: a dataframe\n",
    "        '''\n",
    "        host= cfg.db['host']\n",
    "        port = cfg.db['port']\n",
    "        user = cfg.db['user']\n",
    "        pwd = cfg.db['pwd']\n",
    "        database= cfg.db['database']\n",
    "\n",
    "        con = psycopg2.connect(database=database, user=user, password=pwd, host=host, port=port)\n",
    "\n",
    "        print(\"Database opened successfully\")\n",
    "\n",
    "        sql = \"'''\" + sql_str + \"'''\"\n",
    "        df = sqlio.read_sql_query(sql, con)\n",
    "\n",
    "        return df\n",
    "    \n",
    "    def get_weather(self, df):\n",
    "        '''\n",
    "        request weather information\n",
    "        input: a data frame in which\n",
    "            - first column: date\n",
    "            - second column: location in \"latitude, longitude\"        \n",
    "        output: a dictionary \n",
    "        '''\n",
    "        key = cfg.rapid_api['key']\n",
    "        base_url = \"https://dark-sky.p.rapidapi.com\"\n",
    "        headers = { 'x-rapidapi-host': \"dark-sky.p.rapidapi.com\",\n",
    "                    'x-rapidapi-key': key }\n",
    "        weather_dict = { 'weather':[] }\n",
    "\n",
    "        count = 1\n",
    "        for row in df.values:\n",
    "            print('Query Count: ', count)\n",
    "            date = row[0]\n",
    "            ll = row[1]\n",
    "            url = base_url + '/' + ll + ',' + date + 'T' + '13:00:00'        \n",
    "            res = requests.get(url, headers=headers)\n",
    "            if res.status_code == 200:\n",
    "                weather_json = res.json()\n",
    "                try:\n",
    "                    weather = weather_json['currently']['summary']\n",
    "                except:\n",
    "                    weather = 'NA'\n",
    "                finally:        \n",
    "                    weather_dict['weather'].append(weather)\n",
    "            else:\n",
    "                weather_dict['weather'].append('NA')            \n",
    "            count += 1\n",
    "        return weather_dict\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "9a3ab141-eb1e-4d8b-ac73-f938c5642068",
   "metadata": {},
   "outputs": [],
   "source": [
    "df = pd.read_csv('../data/flights_samp.csv')\n",
    "df_air = pd.read_csv('../data/airports_usa.csv')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 92,
   "id": "d4c1135b-53ba-45b6-b312-ae95e609b4da",
   "metadata": {},
   "outputs": [],
   "source": [
    "df_air = df_air[['IATA_CODE', 'LATITUDE', 'LONGITUDE']]\n",
    "df_air = df_air.rename(columns={'IATA_CODE': 'origin'})"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 94,
   "id": "71aabd4e-c964-4140-8d0a-4113b325626c",
   "metadata": {},
   "outputs": [],
   "source": [
    "top20_airport_code = ['LAX', 'ORD', 'EWR', 'SFO', 'LGA', 'DFW', 'LAS', 'CLT', 'DEN',\n",
    "                      'PHL', 'IAH', 'SEA', 'ATL', 'PHX', 'MCO', 'DTW', 'SLC', 'BOS',\n",
    "                      'JFK', 'MSP']"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 95,
   "id": "d527253e",
   "metadata": {},
   "outputs": [],
   "source": [
    "df = df.merge(df_air, on='origin', how='left')\n",
    "df['ll'] = df.LATITUDE.astype('str') + ',' + df.LONGITUDE.astype('str')\n",
    "df.drop(columns=['LATITUDE', 'LONGITUDE'], inplace=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 96,
   "id": "45d35098",
   "metadata": {},
   "outputs": [],
   "source": [
    "df_origin = df[df.origin.isin(top20_airport_code)]\n",
    "df_origin = df_origin [['fl_date', 'll']]\n",
    "df_origin = df_origin.drop_duplicates().reset_index(drop=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "bb4be85c",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "bootcamp",
   "language": "python",
   "name": "bootcamp"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
