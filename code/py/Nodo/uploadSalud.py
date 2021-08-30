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
                        'PNUD/Producto7/Planillas/nuevo\SJM/PLANILLA_INGRESO.xlsx')

    dataFrame = pd.read_excel(path, sheet_name='Instituciones SALUD')
    headers = dataFrame.columns

    counter = 0
    georeferenced = 0

    featureCollection = []

    for i in range(0, len(dataFrame)):
        name = None  # string
        region = None  # string
        city = None  # string
        address = None  # string
        category1 = None  # string
        category2 = None
        category3 = None
        contact = None  # string
        info = None  # string
        reach = None  # string

        longitude = None
        latitude = None
        coordinates = [0, 0]

        counter += 1

        temp = dataFrame[headers[0]][i]
        if isinstance(temp, str):
            name = temp
        else:
            name = ""

        temp = dataFrame[headers[1]][i]
        if isinstance(temp, str):
            if temp == 'Aysén del Gral. Carlos Ibáñez del Campo':
                region = 'Aysén del General Carlos Ibáñez del Campo'
            else:
                region = temp
        else:
            region = ""

        temp = dataFrame[headers[2]][i]
        if isinstance(temp, str):
            city = (temp)
        else:
            city = ""

        temp = dataFrame[headers[3]][i]
        if temp is not None and isinstance(temp, str):
            address = temp
            tempAddress = temp.split(",")
            addressNumber = tempAddress[0]
            if addressNumber != 'S/N':
                if addressNumber != '':
                    addressNumber = int(tempAddress[0])
            addressStreet = tempAddress[1]

            if addressNumber is not None and addressStreet is not None:
                if type(addressNumber) is not int:
                    longitude = 0
                    latitude = 0
                    coordinates = [longitude, latitude]
                else:
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

        temp = dataFrame[headers[4]][i]
        if isinstance(temp, str):
            category1 = temp
        else:
            category1 = ""
        category2 = "Salud"
        category3 = "sasa"

        temp = dataFrame[headers[5]][i]
        print(temp)
        print(type(temp))
        if isinstance(temp, str):
            contact = temp
        elif isinstance(temp, np.int64):
            contact = str(temp)
        else:
            contact = ""

        temp = dataFrame[headers[6]][i]
        if isinstance(temp, str):
            info = temp
        else:
            info = ""

        temp = dataFrame[headers[7]][i]
        if isinstance(temp, str):
            reach = temp
        else:
            info = ""

        features = {
            'properties': {
                'nombre': name,
                'categoria1': category1,
                'categoria2': category2,
                'categoria3': category3,
                'direccion': address,
                'contacto': contact,
                'informacion': info
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

with open('dataInstitucionesSalud.json', 'w', encoding='utf8') as json_file:
    json.dump(featureCollection, json_file, ensure_ascii=False)
json_file.close()
