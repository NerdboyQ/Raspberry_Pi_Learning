##~ Pandas COVID Data Analysis script
##~ Author : Princton C. Brennan
##~ Created : April 18, 2020
##~ 
##~ Function : This script analyzes COVID-19 data per the John Hopkins provided data
##~            shared with their repository found here: https://github.com/CSSEGISandData/COVID-19.git
##~            The repository is cloned, and then updated each time this script gets ran; 
##~            this is done using a git pull command w/ the gitpython (git) module.
##~

import os, sys, time, glob, git, datetime, argparse
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import figure
from pprint import pprint


start_time = datetime.datetime.now()
def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--state', help='Please provide a state to consider.')
    args = parser.parse_args()
    state = str(args.state)
    if state == 'None':
        return('California')
    return state

def get_max_divisor(plot_point_count):
    val = 10	##~ Setting default value to avoid errors
    for i in range(2,20):
        if plot_point_count%i ==0:
            val = i

    #val = plot_point_count/val
    return val

def add_annotation_to_vertical_graph(plots):
	for plot in plots:
            count = 1
            inter_points = get_max_divisor(len(plot.patches))
            for i in plot.patches:
                if count == inter_points:
		    # get_width pulls left or right; get_y pushes up or down
                    plot.text(i.get_x()-0.5, i.get_height()*0.9, str(i.get_height()), fontsize=8, color='white',rotation=45)
                    plot.set_facecolor('darkgray') 
                    count = 1
                else:
                    count+=1

##~ Check date and time to make sure the data isn't duplicated unnecessarily 
current_date_full = datetime.datetime.today()
current_hour = current_date_full.hour
current_date = current_date_full.strftime('%m-%d-%Y')

if current_hour > 17:
	current_date = current_date + '.csv'
else:
	current_date = current_date_full - datetime.timedelta(days=1)
	current_date = current_date.strftime('%m-%d-%Y')
	current_date = current_date + '.csv'
	
new_df = None
new_df_raw = None

ref_dir = 'COVID-19'
fldr_1 = 'csse_covid_19_data/csse_covid_19_time_series'
fldr_2 = 'csse_covid_19_data/csse_covid_19_daily_reports'
cwd = os.getcwd()
ref_dir = cwd[:cwd.find('Rasp')]+ref_dir
repo = git.Repo(ref_dir)
repo.remotes.origin.pull()

if "|".join(os.listdir()).find(current_date) == -1:
	##~ The try block below works for window's based systems (NOTE: the slashes differ between os's)
	try:
	    path_temp = ref_dir+"/"+fldr_1
	    us_timeSeries_ccases_csv = glob.glob(path_temp+"\\*confirmed_US.csv")[0]
	    us_timeSeries_deaths_csv = glob.glob(path_temp+"\\*deaths_US.csv")[0]

	    us_timeSeries_deaths_df = pd.read_csv(us_timeSeries_deaths_csv)
	    us_timeSeries_ccases_df = pd.read_csv(us_timeSeries_ccases_csv)

	##~ The except block below works for linux' based systems
	except Exception:
	    path_temp = ref_dir+"/"+fldr_1
	    us_timeSeries_ccases_csv = glob.glob(path_temp+"/*confirmed_US.csv")[0]
	    us_timeSeries_deaths_csv = glob.glob(path_temp+"/*deaths_US.csv")[0]

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
	dates_col_df['Dates'] = dates_col_df['Dates'].apply(lambda x: pd.to_datetime(x))
	##|print(dates_col_df['Dates'])
	left_of_df = pd.concat([left_of_df]*duplicate_row_multiplier).sort_index()
	new_df = left_of_df.loc[:,'Province_State':]
	new_df['Date'] = dates_col_df['Dates'].values
	new_df['Deaths'] = values_list_df['Deaths'].values
	new_df = new_df.drop(columns=['Long_','Lat'])
	new_df_raw = new_df
	new_df_raw.to_csv(current_date,index=False)
	#new_df.to_excel('v2_output.xlsx')
else:
	print('found file')
	new_df = pd.read_csv(current_date)
	new_df_raw = new_df

province_list = sorted(new_df['Province_State'].unique())

max_deaths_df = new_df.groupby(['Province_State'],as_index=False)['Deaths'].sum().sort_values(by=['Deaths'],ascending=False).reset_index(drop=True)
max_deaths_df.index+=1
print('-'*50)
print('Top 10 States w/ Highest Death Toll by COVID-19:\n')
print(max_deaths_df.head(10))
##~ Block for state specific history
state = get_arguments()
print('Analysis running for : ' +state)
new_df_raw_fl = new_df_raw[(new_df_raw['Province_State'] == state)]
peak_death = new_df_raw_fl[(new_df_raw_fl['Deaths'] == new_df_raw_fl['Deaths'].max())]
print('-'*50)
print('Peak daily deaths for ' +state +' was ' +str(peak_death['Deaths'].values[0]) +' on ' +str(peak_death['Date'].values[0]))
new_df_raw_fl = new_df_raw_fl.groupby('Date',as_index=False)['Deaths'].sum()
new_df_raw_fl = new_df_raw_fl.sort_values(by=['Date','Deaths']).reset_index(drop=True)
new_df_raw_fl = new_df_raw_fl[(new_df_raw_fl['Deaths'] != 0)]
##~ Block for US specific history
'''new_df_raw = new_df_raw[(new_df_raw['Deaths'] != 0)]
new_df_raw = new_df_raw.groupby('Date',as_index=False)['Deaths'].sum()
new_df_raw = new_df_raw.sort_values(by=['Date','Deaths']).reset_index(drop=True)'''

new_df_raw_fl.to_csv('v2_output.csv')
##|print(new_df_raw_fl.shape)
print('Total death toll for ' +state +' : ' +str(new_df_raw_fl['Deaths'].sum()))
fig2, bx1 = plt.subplots()
bx2 = bx1.twinx()
sub_plot3 = new_df_raw_fl.plot(ax=bx1,x='Date',y='Deaths',kind='bar', title='COVID deaths for US by state: ' +state)
sub_plot4 = new_df_raw_fl.plot(ax=bx2,x='Date',y='Deaths',kind='line',marker='o',color='purple')
fig2.canvas.set_window_title(state +' : COVID TIME SERIES DATA')
add_annotation_to_vertical_graph([sub_plot3])
fig2.subplots_adjust(bottom=0.35,left=0.1,right=0.9,top=0.9)
stop_time = datetime.datetime.now()
run_time = stop_time - start_time
print('Total Runtime : ' +str(run_time))

plt.show()
