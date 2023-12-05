# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 11:06:39 2023

@author: wisoa004
"""


import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

# Laster inn data om alkoholforbruk
file_path = 'alc_consumption_liters_per_capita.csv'  # Erstatt med filstien til din CSV-fil
alc_consumption_data = pd.read_csv(file_path)

# Velger data for året 2015
data_2015 = alc_consumption_data[alc_consumption_data['Year'] == 2015]  # Her kan du velge året

# Endrer navnet på kolonnen for alkoholforbruk for enklere bruk
data_2015 = data_2015.rename(columns={
    "Total alcohol consumption per capita (liters of pure alcohol, projected estimates, 15+ years of age)": "Alcohol_Consumption_Per_Capita"
})

# Laster inn verdenskartet
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Fletter verdenskartet med data fra 2015 om alkoholforbruk
world_map = world.merge(data_2015, left_on='iso_a3', right_on='Code')

# Plotter kloroplett-kartet
fig, ax = plt.subplots(1, 1, figsize=(15, 10))
world_map.plot(column='Alcohol_Consumption_Per_Capita', ax=ax, legend=True,
               legend_kwds={'label': "Alcohol Consumption Per Capita (Liters, 2015)",
                            'orientation': "horizontal"},
               cmap='OrRd')

# Setter tittelen for kartet
plt.title('World Map of Alcohol Consumption Per Capita in 2015')

# Viser plottet
plt.show()


