##
import requests
import pandas as pd

fechaIniStr = '2023-04-01T00:00:00UTC'
fechaFinStr = '2023-05-01T00:00:00UTC'
url = "https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos/" \
      f"fechaini/{fechaIniStr}/fechafin/{fechaFinStr}/todasestaciones"

with open('token_1.txt', 'r') as file:
    api_key = file.read()

querystring = {"api_key": api_key}

headers = {
    'cache-control': "no-cache"
    }

response = requests.request('GET', url, headers=headers, params=querystring).json()
stations_data = requests.request('GET', response['datos'], headers=headers, params=querystring).json()
stations_data = pd.DataFrame(stations_data)

##
def to_float(x):
    if type(x) == str:
        if not(',' in x):
            return 0
        a = list(x)
        for n in range(len(x)):
            if a[n] == ',':
                a[n] = '.'
        return float(''.join(a))
    else:
        return 0

##
stations_data['prec'] = stations_data.prec.apply(to_float)
##
mean_prec = stations_data.groupby('provincia')['prec'].mean()

##

