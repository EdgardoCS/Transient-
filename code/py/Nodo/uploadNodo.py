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

    """
    # Note: this script only works with pymongo 3.8

    client = pymongo.MongoClient("mongodb://localhost:27017/")

    db = client[""]

    destinationCollection = db["full-pscv-mena"]
    """

    # API
    geocoder = Geocoder(
        access_token='pk.eyJ1IjoiZWRnYXJkb3MiLCJhIjoiY2o0OG54eDFjMGFjMzJxcGNlZzBnZnJrMiJ9.B__rQ4ztUAy6hXN7fjJHPw')

    path = os.path.join(Path('C:/Users/Ed/Documents/'),
                        'PNUD/Producto7/Planillas/nuevo\Arica/PLANILLA_INGRESO - Arica v3.xlsx')

    dataFrame = pd.read_excel(path, sheet_name='Nodos (Beneficiarios-as)')
    headers = dataFrame.columns

    counter = 0
    georeferenced = 0

    featureCollection = []

    for i in range(0, len(dataFrame)):
        name = None  # string
        lastName = None  # string
        idNumber = None  # int
        rut = None  # int
        birthDate = None  # date
        sex = None  # string
        phone = None  # int
        mail = None  # string
        region = None  # string
        city = None  # string
        address = None  # string
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
            lastName = temp
        else:
            lastName = ""

        temp = dataFrame[headers[2]][i]
        if isinstance(temp, np.int64):
            idNumber = str(temp)
        elif isinstance(temp, int):
            idNumber = str(temp)
        else:
            idNumber = ""

        temp = dataFrame[headers[3]][i]
        if temp is not None:
            rut = str(temp)
        else:
            rut = ""

        temp = dataFrame[headers[4]][i]
        if temp is not None:
            birthDate = temp.strftime('%Y-%m-%d')
        else:
            birthDate = ""

        temp = dataFrame[headers[5]][i]
        if isinstance(temp, str):
            sex = temp.capitalize()
        else:
            sex = ""

        temp = dataFrame[headers[6]][i]

        print(temp)
        print(type(temp))
        if isinstance(temp, np.int64):
            phone = str(temp)
            print(phone)
        elif isinstance(temp, np.float64):
            phone = str(temp)
            print(phone)
        elif isinstance(temp, int):
            phone = str(temp)
        else:
            phone = ""

        temp = dataFrame[headers[7]][i]
        if isinstance(temp, str):
            mail = temp
        else:
            mail = ""

        temp = dataFrame[headers[8]][i]
        if isinstance(temp, str):
            region = temp
        else:
            region = ""

        temp = dataFrame[headers[9]][i]
        if isinstance(temp, str):
            city = temp
        else:
            city = ""

        temp = dataFrame[headers[10]][i]
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

        features = {
            'rutGestor': '166355974',
            'rut': rut,
            'nombres': name,
            'apellidos': lastName,
            'comuna': city,
            'region': region,
            'fechaNacimiento': birthDate,
            'sexo': sex,
            'id': idNumber,
            'telefono': phone,
            'email': mail,
            'direccion': address,
            'geometry': {
                'type': 'Point',
                'coordinates': coordinates
            },
        }

        print(features)
        featureCollection.append(features)

    with open('dataNodos.json', 'w', encoding='utf8') as json_file:
        json.dump(featureCollection, json_file, ensure_ascii=False)
        json_file.close()
