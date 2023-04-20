##
import requests
import pandas as pd

fechaIniStr = '2021-04-01T00:00:00'
fechaFinStr = '2021-05-01T00:00:00'
idema = '0252D'
url = "https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos/" \
      f"fechaini/{fechaIniStr}/fechafin/{fechaFinStr}/estacion/{idema}"

with open('token_1.txt', 'r') as file:
    api_key = file.read()

querystring = {"api_key": api_key}

headers = {
    'cache-control': "no-cache"
    }

response = requests.request('GET', url, headers=headers, params=querystring).text
