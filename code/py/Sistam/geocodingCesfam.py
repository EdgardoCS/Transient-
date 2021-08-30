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
    destinationCollection = db['cesfamCormuval']

    path = os.path.join(Path('/home/ed/Downloads/Establecimientos APS.xlsx'))

    dataFrame = pd.read_excel(path, sheet_name='Sheet1')

    headers = dataFrame.columns

    counter = 0
    bbox = [-71.72529354311416, -33.167154081918966, -71.53801175418334, -33.00838043513506]

    geocoder = Geocoder(
        access_token='pk.eyJ1IjoiZWRnYXJkb3MiLCJhIjoiY2o0OG54eDFjMGFjMzJxcGNlZzBnZnJrMiJ9.B__rQ4ztUAy6hXN7fjJHPw')

    # print(sheets)

    longitude = None  # AA
    latitude = None  # AB

    for i in range(0, len(dataFrame)):
        totalCounter += 1

        # xlsx data

        establishment = None
        addressStreet = None
        addressNumber = None
        addressCity = None
        manager = None
        phone = None
        some = None
        code_cmv = None
        code_ssvsa = None
        coordinates = [0.0, 0.0]

        temp = dataFrame[headers[10]][i]
        if isinstance(temp, str):
            code_cmv = temp
        else:
            code_cmv = None

        if code_cmv:
            if isinstance(temp, str):
                temp = dataFrame[headers[0]][i]
                if isinstance(temp, str):
                    establishment = temp
                else:
                    establishment = None

                temp = dataFrame[headers[2]][i]
                if isinstance(temp, str):
                    addressStreet = temp
                else:
                    addressStreet = None

                temp = dataFrame[headers[4]][i]
                if isinstance(temp, str):
                    addressCity = temp
                else:
                    addressCity = None

                if addressStreet:
                    temp = dataFrame[headers[3]][i]
                    if not math.isnan(temp):
                        addressNumber = int(temp)
                    else:
                        addressNumber = None

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

                        temp = dataFrame[headers[5]][i]
                        if isinstance(temp, str):
                            manager = temp
                        else:
                            manager = None

                        temp = dataFrame[headers[6]][i]
                        if not math.isnan(temp):
                            phone = int(temp)
                        else:
                            phone = None

                        temp = dataFrame[headers[8]][i]
                        if isinstance(temp, str):
                            some = temp
                        else:
                            some = None

                        temp = dataFrame[headers[11]][i]
                        if not math.isnan(temp):
                            code_ssvsa = int(temp)
                        else:
                            code_ssvsa = None

                        data = {
                            'institucion': {
                                'nombre': establishment,
                                'cod-cmv': code_cmv,
                                'cod-ssvsa': code_ssvsa,
                                'encargado': manager,
                            },
                            'datosContacto': {
                                'direccion': {
                                    'calle': addressStreet,
                                    'numero': addressNumber,
                                    'ciudad': addressCity,
                                    'pais': 'Chile',
                                    'telefono1': phone,
                                    'some': some
                                }
                            },
                            'geometry':
                                {
                                    'type': 'Point',
                                    'coordinates': coordinates
                                },

                        }
                        #print(data)
                        #print('-----------------------')
                        destinationCollection.insert_one(data)

print('located ', counter, 'of', totalCounter)
