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

if __name__ == '__main__':

    # API
    geocoder = Geocoder(
        access_token='pk.eyJ1IjoiZWRnYXJkb3MiLCJhIjoiY2o0OG54eDFjMGFjMzJxcGNlZzBnZnJrMiJ9.B__rQ4ztUAy6hXN7fjJHPw')

    path = os.path.join(Path('C:/Users/Ed/Documents/'),
                        'PNUD/Producto7/Planillas/ViviendasTuteladas.xlsx')

    dataFrame = pd.read_excel(path, sheet_name='Sheet3')
    headers = dataFrame.columns

    counter = 0
    georeferenced = 0

    featureCollection = []

    for i in range(0, len(dataFrame)):
        name = None  # string
        region = None  # string
        city = None  # string
        address = None  # string
        type = None
        category1 = None  # string
        category2 = None  # string
        category3 = None  # string

        longitude = None
        latitude = None
        coordinates = [0, 0]

        counter += 1

        temp = dataFrame[headers[0]][i]
        if isinstance(temp, str):
            type = temp
        else:
            type = ""

        temp = dataFrame[headers[1]][i]
        if isinstance(temp, str):
            name = temp
        else:
            name = ""

        temp = dataFrame[headers[2]][i]
        if isinstance(temp, str):
            region = temp
        else:
            region = ""

        temp = dataFrame[headers[3]][i]
        if isinstance(temp, str):
            city = temp
        else:
            city = ""

        temp = dataFrame[headers[6]][i]
        if temp is not None:
            address = temp
            response = geocoder.forward(temp, types=('address',))
            collection = response.json()
            if 'features' in collection:
                relevance = None

                if len(collection['features']) > 0:

                    longitude = collection['features'][0]['geometry']['coordinates'][0]
                    latitude = collection['features'][0]['geometry']['coordinates'][1]

                    relevance = str(collection['features'][0]['relevance'])
                    georeferenced += 1

                    if float(relevance) >= 0.7:
                        coordinates = [longitude, latitude]
                    else:
                        longitude = 0
                        latitude = 0
                        coordinates = [longitude, latitude]
        else:
            address = ""
            longitude = 0
            latitude = 0
            coordinates = [longitude, latitude]

        features = {
            'properties': {
                'nombre': name,
                'categoria1': 'Servicios públicos',
                'categoria2': 'Servicios sociales',
                'categoria3': 'spsc',
                'direccion': address,
            },
            'geometry': {
                'type': 'Point',
                'coordinates': coordinates
            },
            'tipo': 'institucion',
            'region': region,
            'comuna': city
        }

        print(features)
        featureCollection.append(features)

with open('dataViviendas.json', 'w', encoding='utf8') as json_file:
    json.dump(featureCollection, json_file, ensure_ascii=False)
json_file.close()
