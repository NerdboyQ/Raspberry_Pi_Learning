import os, sys, time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import figure
from pprint import pprint

def create_max_values_df(df,col,unique_keys,target_col):
	df_list = []
	for key in unique_keys:
		df_temp = df[(df[col] == key) ]
		df_temp = df_temp[(df[target_col] == df_temp[target_col].max())]
		df_list.append(df_temp.head(1))
	df_out = pd.concat(df_list).sort_values(by=target_col,ascending=False)._index(drop=True)
	df_out.index+=1
	return df_out

def add_annotation_to_vertical_graph(plots):
	for plot in plots:
		'''totals = []
		for i in plot.patches:
			#|print(i.get_height())
			totals.append(i.get_height())

		total = sum(totals)'''

		for i in plot.patches:
		    # get_width pulls left or right; get_y pushes up or down
		    plot.text(i.get_x()+0.05, i.get_height()*1.01, str(i.get_height()), fontsize=8, color='white',rotation=45)
		plot.set_facecolor('darkgray') 



df_states = pd.read_csv("state_territory_abbreviations.csv")

df_og_death = pd.read_csv('Provisional_Death_Counts_for_Coronavirus_Disease__COVID-19.csv')
df_og_cases = pd.read_csv('States Reporting Cases of COVID-19 to CDC_.csv')
df_og_world = pd.read_csv('world_ecdc_data.csv')

df_og_world['dateRep'] = df_og_world['dateRep'].apply(lambda x: pd.to_datetime(x))	##converts all the rows to datetime format
countries_list = df_og_world['countriesAndTerritories'].unique()
df_max_cases_by_country = create_max_values_df(df_og_world,'countriesAndTerritories',countries_list,'cases')
df_max_cases_by_country = df_max_cases_by_country[['dateRep','cases','countriesAndTerritories']]
df_max_deaths_by_country = create_max_values_df(df_og_world,'countriesAndTerritories',countries_list,'deaths')
df_max_deaths_by_country = df_max_deaths_by_country[['dateRep','deaths','countriesAndTerritories']]

'''print("-"*100)
print("Max cases by country:")
print(df_max_cases_by_country.head(10))
print("-"*100)
print("Max deaths by country:")
print(df_max_deaths_by_country.head(10))'''

df = df_og_world[(df_og_world['countriesAndTerritories'] == 'United_States_of_America')]
df = df[['dateRep','month','countriesAndTerritories','deaths']]
df = df.sort_values(by='dateRep')
#df = df[(df['deaths'] > 10)]
'''print("-"*100)
print("Full death list by country:")
print(df)'''
fig1, ax = plt.subplots()
ax2 = ax.twinx()

sub_plot1 = df_max_deaths_by_country.head(10).plot(ax=ax,x='countriesAndTerritories',y='deaths',kind='bar', title='Data collected from the ECDC (Europe Center for Disease Control)',color ='darkred',legend=False)
sub_plot2 = df_max_cases_by_country.head(10).plot(ax=ax2,x='countriesAndTerritories',y='cases',kind='line',color ='darkorange')
ax.set_ylabel('COVID Deaths')
ax2.set_ylabel('COVID Cases',labelpad=20)

#~Creating one legend of the combined subplots
lines, labels = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc=0)

fig1.canvas.set_window_title('COVID WORLD DATA - Country Deaths x Country Cases')
fig2, bx = plt.subplots()
sub_plot3 = df.plot(ax=bx,x='dateRep',y='deaths',kind='bar', title='COVID deaths for US')
fig2.canvas.set_window_title('COVID WORLD DATA')

#fig1.subplots_adjust(bottom=0.5, right=0.8, top=0.9)
#fig2.subplots_adjust(bottom=0.5, right=0.8, top=0.9)
add_annotation_to_vertical_graph([sub_plot1,sub_plot2])

mng = plt.get_current_fig_manager()
og_fig_size = fig1.get_size_inches() 
#|print(og_fig_size)
fig1.set_size_inches(og_fig_size[0]*2,og_fig_size[1])
fig2.set_size_inches(og_fig_size[0]*2,og_fig_size[1])
#|print(fig1.get_size_inches())

fig1.subplots_adjust(bottom=0.5, left=.1,right=0.9, top=0.95)
fig2.subplots_adjust(bottom=0.5, left=.1,right=0.9, top=0.95)
#|fig1.savefig(fig1.canvas.get_window_title() + '.png')
plt.show()