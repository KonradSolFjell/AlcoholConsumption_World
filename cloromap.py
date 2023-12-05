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

# Be brukeren om å velge et årstall
gyldige_år = [2000, 2005, 2010, 2015, 2018]
valgt_år = int(input(f"Velg et årstall fra listen {gyldige_år}: "))

while valgt_år not in gyldige_år:
    print("Ugyldig årstall. Prøv igjen.")
    valgt_år = int(input(f"Velg et årstall fra listen {gyldige_år}: "))

# Velger data for det valgte året
valgt_data = alc_consumption_data[alc_consumption_data['Year'] == valgt_år]

# Endrer navnet på kolonnen for alkoholforbruk for enklere bruk
valgt_data = valgt_data.rename(columns={
    "Total alcohol consumption per capita (liters of pure alcohol, projected estimates, 15+ years of age)": f"Alcohol_Consumption_Per_Capita_{valgt_år}"
})

# Laster inn verdenskartet
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Fletter verdenskartet med data for det valgte året om alkoholforbruk
world_map = world.merge(valgt_data, left_on='iso_a3', right_on='Code')

# Plotter kloroplett-kartet
fig, ax = plt.subplots(1, 1, figsize=(15, 10))
world_map.plot(column=f'Alcohol_Consumption_Per_Capita_{valgt_år}', ax=ax, legend=True,
               legend_kwds={'label': f"Alcohol Consumption Per Capita (Liters, {valgt_år})",
                            'orientation': "horizontal"},
               cmap='OrRd')

# Setter tittelen for kartet
plt.title(f'World Map of Alcohol Consumption Per Capita in {valgt_år}')

# Viser plottet
plt.show()


