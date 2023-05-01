##
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely import points
spain = gpd.read_file('https://geodata.ucdavis.edu/gadm/gadm4.1/json/gadm41_ESP_0.json', encoding='utf-8').explode().geometry[0]

with open('stations_data.csv', 'r') as file:
    stations_data = pd.read_csv(file)
stations_data = stations_data[['latitude', 'longitude', 'zone']]

zone_1 = list(stations_data[stations_data.zone == 1][['longitude', 'latitude']].values)
zone_2 = list(stations_data[stations_data.zone == 2][['longitude', 'latitude']].values)

d = []
for r in [zone_1, zone_2]:
    c = []
    for s in r:
        c += [points(s)]
    d += [c]

zone_1 = gpd.GeoSeries(d[0])
zone_2 = gpd.GeoSeries(d[1])
##
canarias_isles = spain[:18]
ceuta_melilla = spain[18:20]
remaining_spain = spain[29:]

fig, ax = plt.subplots(figsize=(10, 10))
remaining_spain.plot(ax=ax)
zone_1.plot(ax=ax)
plt.show()
##
ax = remaining_spain.plot()
ceuta_melilla.plot(ax=ax)

plt.show()
