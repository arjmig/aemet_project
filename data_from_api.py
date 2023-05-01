##
import requests
import pandas as pd
with open('token_1.txt', 'r') as file:
    api_key = file.read()
querystring = {"api_key": api_key}
headers = {
    'cache-control': "no-cache"
    }


def to_float(x):
    if type(x) == str:
        if not (',' in x):
            return 0
        a = list(x)
        for n in range(len(x)):
            if a[n] == ',':
                a[n] = '.'
        return float(''.join(a))
    else:
        return 0

all_aprils = []
stations_by_year = []
for n in range(2000, 2024):
    fechaIniStr = f'{n}-04-01T00:00:00UTC'
    fechaFinStr = f'{n}-05-01T00:00:00UTC'
    url = "https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos/" \
          f"fechaini/{fechaIniStr}/fechafin/{fechaFinStr}/todasestaciones"
    response = requests.request('GET', url, headers=headers, params=querystring).json()
    stations_data = requests.request('GET', response['datos'], headers=headers, params=querystring).json()
    stations_data = pd.DataFrame(stations_data)
    stations_data['prec'] = stations_data.prec.apply(to_float)
    province_prec = stations_data.groupby('indicativo').prec.sum()
    all_aprils += [province_prec]

all_aprils = pd.concat(all_aprils, axis=1)

fill_values = all_aprils.mean(axis=1)

all_aprils = all_aprils.apply(lambda x: x.fillna(fill_values))

all_aprils.columns = range(2000, 2024)

url = "https://opendata.aemet.es/opendata/api/valores/climatologicos/inventarioestaciones/todasestaciones"
response = requests.request('GET', url, headers=headers, params=querystring).json()
station_location = requests.request('GET', response['datos'], headers=headers, params=querystring).json()
station_location = pd.DataFrame(station_location)[['latitud', 'longitud', 'indicativo', 'provincia']].groupby('indicativo').apply(
    lambda x: x.iloc[0])[['latitud', 'longitud', 'provincia']]

def zones(x):
    if (x == 'LAS PALMAS') or (x == 'STA. CRUZ DE TENERIFE'):
        return 2
    else:
        return 1

station_location['provincia'] = station_location['provincia'].apply(zones)

def convert_coor(x):
    degrees = int(x[:2])
    minutes = int(x[2:4])
    seconds = int(x[4:6])
    sign = x[6]
    add_up = degrees + minutes/60 + seconds/3600
    if sign == 'W' or sign == 'S':
        add_up = -add_up
    return add_up

station_location['latitud'] = station_location['latitud'].apply(lambda x: convert_coor(x))
station_location['longitud'] = station_location['longitud'].apply(lambda x: convert_coor(x))
station_location.index.rename(None, inplace=True)
station_location.rename(columns={'latitud': 'latitude', 'longitud': 'longitude', 'provincia': 'zone'}, inplace=True)


all_aprils['latitude'] = station_location['latitude']
all_aprils['longitude'] = station_location['longitude']


with open('prec_data.csv', 'w') as file:
    all_aprils.to_csv(file)

with open('stations_data.csv', 'w') as file:
    station_location.to_csv(file)





##

