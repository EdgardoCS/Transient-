import os
import json
import time
import math
import pymongo
import datetime
import numpy as np
import pandas as pd
from pathlib import Path
from mapbox import Geocoder
from pandas.io.json import json_normalize

if __name__ == '__main__':

    # API
    geocoder = Geocoder(
        access_token='pk.eyJ1IjoiZWRnYXJkb3MiLCJhIjoiY2o0OG54eDFjMGFjMzJxcGNlZzBnZnJrMiJ9.B__rQ4ztUAy6hXN7fjJHPw')

    path = os.path.join(Path('C:/Users/Ed/Documents/'),
                        'PNUD/Producto7\Geodata\Cuarteles.xlsx')

    dataFrame = pd.read_excel(path, sheet_name='EST2')
    headers = dataFrame.columns

    counter = 0
    georeferenced = 0

    featureCollection = []

    for i in range(0, len(dataFrame)):
        name = None  # string
        region = None  # string
        city = None  # string
        address = None  # string
        contact = None  # string
        info = None  # string
        reach = None  # string

        longitude = None
        latitude = None
        coordinates = [0, 0]

        counter += 1

        temp = dataFrame[headers[4]][i]
        if isinstance(temp, str):
            name = temp
        else:
            name = ""

        temp = dataFrame[headers[1]][i]
        if isinstance(temp, str):
            region = temp
        else:
            region = ""

        temp = dataFrame[headers[3]][i]
        if isinstance(temp, str):
            city = (temp)
        else:
            city = ""
        # print(region, ",", city)

        temp = dataFrame[headers[9]][i]
        if isinstance(temp, str):
            address = temp
        else:
            address = ""
        # print(address)

        temp = dataFrame[headers[11]][i]
        longitude = temp
        temp = dataFrame[headers[10]][i]
        latitude = temp

        coordinates = [latitude, longitude]
        # print(coordinates)

        features = {
            'properties': {
                'nombre': name,
                'categoria1': "Servicios públicos",
                'categoria2': "Seguridad Ciudadana",
                'categoria3': "spsc",
                'direccion': address,
                'contacto': "",
                'informacion': ""
            },
            'geometry': {
                'type': 'Point',
                'coordinates': coordinates
            },
            'tipo': 'institucion',
            'region': region,
            'comuna': city
        }

        # print(features)
        featureCollection.append(features)

with open('dataComisarias.json', 'w', encoding='utf8') as json_file:
    json.dump(featureCollection, json_file, ensure_ascii=False)
json_file.close()
