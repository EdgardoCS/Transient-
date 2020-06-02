import os
import pymongo
import datetime
import numpy as np
import pandas as pd
import math
from pathlib import Path
from mapbox import Geocoder

if __name__ == '__main__':

    counter = 0
    totalCounter = 0
    ##
    # Note: this script only works with pymongo 3.8
    client = pymongo.MongoClient("mongodb://localhost:27017/")

    db = client['demo']

    ##
    destinationCollection = db['listadoEleam']

    path = os.path.join(Path('/home/ed/Downloads/ListadoELEAM.xlsX'))

    dataFrame = pd.read_excel(path, sheet_name='ListadoELEAM')

    headers = dataFrame.columns

    counter = 0
    bbox = [-71.7765564962062, -33.65138558397063, -70.444708719306, -32.599571419268976]

    geocoder = Geocoder(
        access_token='pk.eyJ1IjoiZWRnYXJkb3MiLCJhIjoiY2o0OG54eDFjMGFjMzJxcGNlZzBnZnJrMiJ9.B__rQ4ztUAy6hXN7fjJHPw')

    longitude = None  # AA
    latitude = None  # AB

    for i in range(1, 148):
        totalCounter += 1

        # xlsx data
        code = None
        doc = None
        digit = None
        name = None
        addressStreet = None
        addressNumber = None
        addressCity = None
        phone = None
        mail = None
        webPage = None
        Type = None
        coordinates = [0.0, 0.0]

        temp = dataFrame[headers[0]][i]
        if isinstance(temp, str):
            code = temp

        temp = dataFrame[headers[1]][i]
        if isinstance(temp, str):
            tempRut = temp.split('-')
            if len(tempRut) > 1:
                docType = 'rut'
                doc = tempRut[0].strip()
                digit = tempRut[1].strip()

        temp = dataFrame[headers[2]][i]
        if isinstance(temp, str):
            name = temp

        temp = dataFrame[headers[5]][i]
        if isinstance(temp, str):
            addressStreet = temp

        temp = dataFrame[headers[7]][i]
        if isinstance(temp, str):
            addressCity = temp

        temp = dataFrame[headers[6]][i]
        if not math.isnan(temp):
            addressNumber = int(temp)
        else:
            addressNumber = ""

        if addressNumber:
            response = geocoder.forward(str(addressNumber) + ', ' + addressStreet, bbox=bbox,
                                        types=('address',))

            collection = response.json()

            if len(collection['features']) > 0:
                counter += 1

                longitude = collection['features'][0]['geometry']['coordinates'][0]
                latitude = collection['features'][0]['geometry']['coordinates'][1]
                coordinates = [longitude, latitude]

            else:
                longitude = 0.0
                latitude = 0.0
                coordinates = [longitude, latitude]

        temp = dataFrame[headers[9]][i]
        if not math.isnan(temp):
            phone = temp

        temp = dataFrame[headers[10]][i]
        if isinstance(temp, str):
            mail = temp

        temp = dataFrame[headers[11]][i]
        if isinstance(temp, str):
            webPage = temp

        temp = dataFrame[headers[15]][i]
        if isinstance(temp, str):
            type = temp

        data = {
            'informacionPersonal': {
                'datosPersonales': {
                    'documento': {
                        'tipo': 'rut',
                        'numero': doc,
                        'digitoVerificador': digit
                    },
                    'nombre': name,
                    'tipo': type
                },
                'datosContacto': {
                    'direccion': {
                        'calle': addressStreet,
                        'numero': addressNumber,
                        'ciudad': addressCity,
                        'pais': 'Chile',
                        'telefono1': phone,
                        'e-mail': mail,
                        'sitio': webPage
                    }
                },
                'geometry':
                    {
                        'type': 'Point',
                        'coordinates': coordinates
                    },
            }
        }
        # print(data)
        # print('-----------------------')
        destinationCollection.insert_one(data)

print('located ', counter, 'of', totalCounter)
