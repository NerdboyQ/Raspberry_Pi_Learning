##~ Pandas COVID Data Analysis script
##~ Author : Princton C. Brennan
##~ Created : April 18, 2020
##~ 
##~ Function : This script analyzes COVID-19 data per the John Hopkins provided data
##~            shared with their repository found here: https://github.com/CSSEGISandData/COVID-19.git
##~            The repository is cloned, and then updated each time this script gets ran; 
##~            this is done using a git pull command w/ the gitpython (git) module.
##~

import os, sys, time, glob, git
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import figure
from pprint import pprint

ref_dir = 'COVID-19'
fldr_1 = 'csse_covid_19_data/csse_covid_19_time_series'
fldr_2 = 'csse_covid_19_data/csse_covid_19_daily_reports'
cwd = os.getcwd()
ref_dir = cwd[:cwd.find('Rasp')]+ref_dir
repo = git.Repo(ref_dir)
repo.remotes.origin.pull()
path_temp = ref_dir+"/"+fldr_1
us_timeSeries_ccases_csv = glob.glob(path_temp+"\\*confirmed_US.csv")[0]
us_timeSeries_deaths_csv = glob.glob(path_temp+"\\*deaths_US.csv")[0]

us_timeSeries_deaths_df = pd.read_csv(us_timeSeries_deaths_csv)
us_timeSeries_ccases_df = pd.read_csv(us_timeSeries_ccases_csv)


left_of_df = us_timeSeries_deaths_df.loc[:,:'Population']
right_of_df = us_timeSeries_deaths_df.loc[:,'Population':].drop(columns=['Population']) 
#print("left: " +str(left_of_df.shape[0]) +" vs. right: " +str(right_of_df.shape[0]))
dates_col_df = pd.DataFrame({'Dates' : right_of_df.columns.values})
duplicate_row_multiplier = len(dates_col_df)
dates_col_df = pd.concat([dates_col_df]*left_of_df.shape[0])

#dates_col_df['Dates'] = dates_col_df['Dates'].apply(lambda x: pd.to_datetime(x))

#print(dates_col_df.iloc[87])
values_list = []
for i in range (0,left_of_df.shape[0]):
	for val in right_of_df.iloc[i].values:
		values_list.append(val)

values_list_df = pd.DataFrame({'Deaths' : values_list})
#print("number of death values: " +str(len(values_list)))
left_of_df = pd.concat([left_of_df]*duplicate_row_multiplier).sort_index()
new_df = left_of_df.loc[:,'Province_State':]
new_df['Date'] = dates_col_df['Dates'].values
new_df['Deaths'] = values_list_df['Deaths'].values
new_df = new_df.drop(columns=['Long_','Lat'])

#new_df.to_excel('v2_output.xlsx')
new_df.to_csv('v2_output.csv')
province_list = sorted(new_df['Province_State'].unique())
max_list = []
for province in province_list:
	temp_df = new_df[(new_df['Province_State'] == province)]
	temp_df = temp_df[(temp_df['Deaths'] == temp_df['Deaths'].max())]
	print('='*100)
	print(temp_df.head(1))
	if len(temp_df) > 0:
		max_list.append(temp_df.head(1))
#print(province_list)
us_max_deaths_df = pd.concat(max_list).sort_values(by=['Deaths'],ascending=False).reset_index(drop=True)
us_max_deaths_df.index+=1
print(us_max_deaths_df.head(10))
print(us_max_deaths_df.tail(10))