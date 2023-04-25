##
import requests
import pandas as pd

with open('token_1.txt', 'r') as file:
    api_key = file.read()
querystring = {"api_key": api_key}
headers = {
    'cache-control': "no-cache"
    }

url = "https://opendata.aemet.es/opendata/api/valores/climatologicos/inventarioestaciones/todasestaciones"

response = requests.request('GET', url, headers=headers, params=querystring).json()
metadata = requests.request('GET', response['metadatos'], headers=headers, params=querystring).text
data = requests.request('GET', response['datos'], headers=headers, params=querystring).json()

coordinates = {'latitude': [], 'longitude': [], 'province': []}

for station in data:
    coordinates['latitude'] += [station['latitud']]
    coordinates['longitude'] += [station['longitud']]
    coordinates['province'] += [station['provincia']]

coordinates = pd.DataFrame(coordinates)
##
stat_per_prov = coordinates.groupby('province').latitude.count()