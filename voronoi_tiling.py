##
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
spain = gpd.read_file('https://geodata.ucdavis.edu/gadm/gadm4.1/json/gadm41_ESP_0.json', encoding='utf-8').explode().geometry

canarias_isles = spain[:18]
ceuta_melilla = spain[18:20]
remaining_spain = spain[29:]

canarias_isles.plot()
ax = remaining_spain.plot()
ceuta_melilla.plot(ax=ax)

plt.show()
