##~ This code is an example of pandas and understanding dataframes (df)
##~ DataFrame - a 2 dimensional, size-mutable, tabular data set
##~ (Basically a variable array of data with dynamic dimensions) 
##~ 
##~ This data can easily be manipulated like excel (i.e. filters, sort, averages, etc),
##~ but much faster as it runs in python. 
##~ NOTE:: It can read csv, excel, & txt files (w/ delimiters i.e. ';' or ':')
##~

import pandas as pd


df_pokemon = pd.read_csv("pokemon_data.csv")
##~ Get the headers; they are referred to as columns
##~ The type - Index
headers = df_pokemon.columns
print("Column Headers:\n")
print(headers)

##~ Describe provides a brief analysis of the data in the df
##~ or the same analysis over one column or a range of specified columns
print("High Level DataFrame Analysis description:\n")
print(df_pokemon.describe())

##~ Create new dataframes from the original based on column value conditions
condition_grass_types = (df_pokemon['Type 1'] == 'Grass')
condition_water_types = (df_pokemon['Type 1'] == 'Water')

##~ You can leave out the reset_index method, but that will cause the index
##~ to be inherited from the original dataframe. To create a new index, include
##~ the reset_index method and set the drop argument to True. By default, the
##~ drop argument is set tot False, and this this will add the old index values
##~ to your new dataframe as a new column. Setting this value to True, will
##~ remove that potential index column.
df_grass_types = df_pokemon[condition_grass_types].reset_index(drop=True)
df_water_types = df_pokemon[condition_water_types].reset_index(drop=True)

print("New filtered Grass type DataFrame:\n")
print(df_grass_types)
print("New filtered Water type DataFrame:\n")
print(df_water_types)

##~ Specific columns can be listed as condensed dataframes.
print("Printing specific columns from the grass dataframe:\n")
print(df_grass_types[['Name','HP']])


##~ Create a new dataframe by concatenating, or linking, dataframes
##~ with similar data (i.e. same column headers and column count)
df_water_n_grass = pd.concat([df_grass_types,df_water_types])
print("Concat of Grass  Water Type pokémon dataframes:\n")
print(df_water_n_grass)


##~ The dataframe can be sorted by columns. Below it gets sorted by the
##~ 'HP' column in a descending order by setting the ascending argument to
##~ False.
df_water_n_grass_sorted = df_water_n_grass.sort_values(by=['HP'],ascending=False)
print("Sorted Grass & Water Type Pokemon dataframe:\n")
print(df_water_n_grass_sorted)


##~ The highest value for the HP column is found below specifically for the
##~ pokémon with a 'Water' Type 1. The 'iloc' refer to the index locations
##~ of a dataframe.
max_hp_water_type = df_water_n_grass_sorted[(df_water_n_grass_sorted['Type 1'] == 'Water') & (df_water_n_grass_sorted['HP'] == df_water_n_grass_sorted['HP'].max())]
max_hp_water_type_row = df_water_n_grass_sorted.iloc[max_hp_water_type.index.tolist()]
print("Max hp for water type:\n")
print(max_hp_water_type_row)
