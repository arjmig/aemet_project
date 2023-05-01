##
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
spain = gpd.read_file('https://geodata.ucdavis.edu/gadm/gadm4.1/json/gadm41_ESP_0.json', encoding='utf-8').explode().geometry

with open('stations_data.csv', 'r') as file:
    stations_data = pd.read_csv(file)

zone_1 = stations_data[stations_data.zone == 1]
zone_2 = stations_data[stations_data.zone == 2]

canarias_isles = spain[:18]
ceuta_melilla = spain[18:20]
remaining_spain = spain[29:]

fig, ax = plt.subplots(figsize=(12, 10))
remaining_spain.plot(ax=ax)
zone_1.plot(ax=ax)
plt.show()
##
ax = remaining_spain.plot()
ceuta_melilla.plot(ax=ax)

plt.show()
