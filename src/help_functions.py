{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "dd9c6291",
   "metadata": {},
   "outputs": [],
   "source": [
    "import numpy as np\n",
    "import pandas as pd\n",
    "import seaborn as sns\n",
    "import matplotlib.pyplot as plt\n",
    "import requests\n",
    "from sklearn.preprocessing import StandardScaler\n",
    "import config as cfg"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "0136e947",
   "metadata": {},
   "outputs": [],
   "source": [
    "df = pd.read_csv('../data/flights_samp.csv')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 18,
   "id": "b433df97",
   "metadata": {},
   "outputs": [],
   "source": [
    "def split_numeric_categorical(df, numeric=True):\n",
    "    '''    \n",
    "    Return either numerical columns, or categorical columns in a data frame\n",
    "    numeric: default True, return dataframe of all numerical columns    \n",
    "    input: a data frame\n",
    "    output: a data frame    \n",
    "    '''\n",
    "    numeric_data = df.select_dtypes(include=[np.number])\n",
    "    categorical_data = df.select_dtypes(include='category')\n",
    "    if numeric:\n",
    "        return numeric_data\n",
    "    else:\n",
    "        return categorical_data"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 82,
   "id": "7a18b2f3",
   "metadata": {},
   "outputs": [],
   "source": [
    "def make_categorical(df, cols):\n",
    "    '''\n",
    "    Convert columns in `cols` to type `categorical`\n",
    "    input: df - data frame, cols - a list of columns\n",
    "    output: a copy of the data frame with the converted columns\n",
    "    '''\n",
    "    col_dict = {col:'category' for col in cols}\n",
    "    df = df.astype(col_dict)\n",
    "    return df"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "36de403c",
   "metadata": {},
   "outputs": [],
   "source": [
    "def to_hhmmss(df_time_col):\n",
    "    '''\n",
    "    Change the format of the time in hhmm\n",
    "    to hh:mm:ss, where ss is 00 in this case\n",
    "    Input: `df_time_col`: a Pandas Series\n",
    "    Return: a Pandas Series\n",
    "    '''\n",
    "    \n",
    "    hhmm = []\n",
    "    crs_hm = df_time_col.astype('str')\n",
    "    for t in crs_hm:\n",
    "        if len(t) == 1:\n",
    "            hhmm.append('0' + t + ':00:00')\n",
    "        elif (len(t) == 2) & (t < '24'):\n",
    "            hhmm.append(t + ':00:00')\n",
    "        elif (len(t) == 2) & (t > '24'):\n",
    "            hhmm.append('00:' + t + ':00')\n",
    "        elif len(t) == 3:\n",
    "            hhmm.append('0' + t[0] + ':' + t[1:] + ':00')\n",
    "        else:\n",
    "            hhmm.append(t[:2] + ':' + t[2:] + \":00\")\n",
    "    return hhmm"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "09c4d68e",
   "metadata": {},
   "outputs": [],
   "source": [
    "def to_city_state(city_state_col):\n",
    "    '''\n",
    "    Change the format of `city1/city2, state`\n",
    "    to `city1, state` \n",
    "    Input: A Pandas Series\n",
    "    Output: A Pandas Series\n",
    "    '''\n",
    "    return pd.Series(map(lambda x: x[0].split('/')[0] + ',' + x[-1].strip() ,\n",
    "                    city_state_col.str.split(',')))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 83,
   "id": "e2d33a31",
   "metadata": {},
   "outputs": [],
   "source": [
    "def to_hhmmss(df_time_col):\n",
    "    '''\n",
    "    Change the format of the time in hhmm\n",
    "    to hh:mm:ss, where ss is 00 in this case\n",
    "    Input: `df_time_col`: a Pandas Series\n",
    "    Return: a Pandas Series\n",
    "    '''\n",
    "    \n",
    "    hhmm = []\n",
    "    crs_hm = df_time_col.astype('str')\n",
    "    for t in crs_hm:\n",
    "        if len(t) == 1:\n",
    "            hhmm.append('0' + t + ':00:00')\n",
    "        elif (len(t) == 2) & (t < '24'):\n",
    "            hhmm.append(t + ':00:00')\n",
    "        elif (len(t) == 2) & (t > '24'):\n",
    "            hhmm.append('00:' + t + ':00')\n",
    "        elif len(t) == 3:\n",
    "            hhmm.append('0' + t[0] + ':' + t[1:] + ':00')\n",
    "        else:\n",
    "            hhmm.append(t[:2] + ':' + t[2:] + \":00\")\n",
    "    return hhmm"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "3bebd71f",
   "metadata": {},
   "outputs": [],
   "source": [
    "def merge_df_dict(df_time_ll, dic):\n",
    "    '''\n",
    "    Make a new dataframe with weather column,\n",
    "    then merge the new dataframe with original dataframe\n",
    "    input: df_time_ll, the dataframe where the `dic` is going to be concatenated on\n",
    "    return: The joined version of original dataframe\n",
    "    '''\n",
    "    df_time_ll = pd.concat([df_time_ll, pd.DataFrame.from_dict(dic)], axis=1)\n",
    "    df = df.merge(df_time_ll, on=['fl_date', 'll'], how='left')\n",
    "    return df"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 29,
   "id": "83bc0da3",
   "metadata": {},
   "outputs": [],
   "source": [
    "def to_dummies(df, col_array):\n",
    "    '''\n",
    "    change the given columns into dummy variables\n",
    "    and return the dataframe\n",
    "    '''\n",
    "    return pd.get_dummies(df, columns= col_array, drop_first=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 55,
   "id": "5868d295",
   "metadata": {},
   "outputs": [],
   "source": [
    "def to_scale(df, col_array):\n",
    "    '''\n",
    "    scale the numeric variables to center around 0\n",
    "    and standard deviation of 1\n",
    "    '''\n",
    "    sc = StandardScaler()\n",
    "    df[col_array] = pd.DataFrame(sc.fit_transform(df[col_array]))   "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 56,
   "id": "d859839b",
   "metadata": {},
   "outputs": [],
   "source": [
    "def inverse_scale(df, col_array, sc):    \n",
    "    '''\n",
    "    inverse scale back to the original numeric values\n",
    "    '''\n",
    "    df[col_array] = pd.DataFrame(sc.inverse_transform(df[col_array]))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "d1c5f6a5",
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "2ecec435",
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