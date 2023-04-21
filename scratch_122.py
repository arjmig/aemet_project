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

for n in range(2000, 2024):
    fechaIniStr = f'{n}-04-01T00:00:00UTC'
    fechaFinStr = f'{n}-05-01T00:00:00UTC'
    url = "https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos/" \
          f"fechaini/{fechaIniStr}/fechafin/{fechaFinStr}/todasestaciones"
    response = requests.request('GET', url, headers=headers, params=querystring).json()
    stations_data = requests.request('GET', response['datos'], headers=headers, params=querystring).json()
    stations_data = pd.DataFrame(stations_data)
    stations_data['prec'] = stations_data.prec.apply(to_float)
    mean_prec = stations_data.groupby('provincia').prec.mean()
    mean_prec = mean_prec.reset_index()
    all_aprils += [mean_prec]
##
all_aprils = pd.concat(all_aprils).reset_index(drop=True)
all_aprils['label'] = all_aprils.index
all_aprils.sort_values(['provincia', 'label'], inplace=True)


##

