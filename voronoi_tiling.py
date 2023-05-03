##
import pandas as pd
import geopandas as gpd
from geopandas.tools import overlay
import numpy as np
import matplotlib.pyplot as plt
from shapely import points, Polygon
from scipy.spatial import Voronoi

spain = gpd.read_file('https://geodata.ucdavis.edu/gadm/gadm4.1/json/gadm41_ESP_0.json', encoding='utf-8').explode(index_parts=True).geometry[0]
spain = spain.to_crs(epsg=32630)
remaining_spain = gpd.GeoDataFrame(spain[(spain.index >= 29) + (spain.index.isin([18, 19]))])
canarias_isles = gpd.GeoDataFrame(spain)
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
    c = gpd.GeoSeries(c)
    c.set_crs(epsg=4326, inplace=True)
    c = c.to_crs(epsg=32630)
    d += [c]

zone_1 = d[0]
zone_2 = d[1]

c = []

for zone in [zone_1, zone_2]:
    d = []
    for point in zone:
        d += [[point.x, point.y]]
    c += [d]

np_zone_1 = np.array(c[0])
np_zone_2 = np.array(c[1])

vor = Voronoi(np_zone_1)

polygons = [Polygon(vor.vertices[region]) for region in vor.regions if -1 not in region]
polygons = gpd.GeoDataFrame(geometry=polygons, crs=32630)
polygons = polygons.overlay(remaining_spain, how='intersection')
polygons = polygons.overlay(remaining_spain, how='union')

fig, ax = plt.subplots()
polygons.plot(ax=ax, markersize=3.5, edgecolor='black')
zone_1.plot(ax=ax, markersize=3.5, color='red')
plt.show()

