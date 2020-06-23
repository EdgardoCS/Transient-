import os
import time
import math
import pymongo
import datetime
import numpy as np
import pandas as pd
from pathlib import Path
from datetime import date
from mapbox import Geocoder
from dateutil.relativedelta import relativedelta

if __name__ == '__main__':

    counter = 0
    totalCounter = 0
    ##
    # Note: this script only works with pymongo 3.8
    client = pymongo.MongoClient("mongodb://localhost:27017/")

    db = client['demo']

    destinationCollection = db['personasIncendio']

    path = os.path.join(Path('/home/ed/Downloads/Reporte FIBE Adultos mayores-recuperacion (1).xlsx'))

    dataFrame = pd.read_excel(path, sheet_name='Adultos Mayores')

    headers = dataFrame.columns

    geocoder = Geocoder(
        access_token='pk.eyJ1IjoiZWRnYXJkb3MiLCJhIjoiY2pvNG04eXRyMTh6eTNwcG83Y3BtbXVqZyJ9.x1DfP7ZYKfOoV_tz17Qq2w')

    # print(sheets)

    longitude = None  # AA
    latitude = None  # AB

    for i in range(0, len(dataFrame)):
        totalCounter += 1

        # xlsx data

        doc = None
        digit = None
        name = ""
        lastName1 = ""
        lastName2 = ""
        gender = ""
        birthDate = '1900-01-01'
        phone1 = ""
        address = ""
        city = 'Valparaiso'
        p05 = ""
        p04 = ""
        p06 = ""
        palimento = False
        pagua = False
        psalud = False
        pcolchon = False
        pdiscapacidad = False
        phabitacional = False

        relevance = None
        coordinates = [0.0, 0.0]

        temp = dataFrame[headers[12]][i]  # .replace(u'\xa0', u'')

        if isinstance(temp, np.int64):
            doc = int(temp)
        temp = dataFrame[headers[13]][i]
        if temp:
            digit = temp

        if doc:
            totalCounter += 1

            # Name
            temp = dataFrame[headers[14]][i]
            if pd.isnull(temp):
                name = ""
            elif isinstance(temp, str):
                name = temp
            else:
                name = ""

            # lastName
            temp = dataFrame[headers[15]][i]
            if pd.isnull(temp):
                lastName1 = ""
            elif isinstance(temp, str):
                lastName1 = temp
            else:
                lastName1 = ""

            temp = dataFrame[headers[16]][i]
            if pd.isnull(temp):
                lastName2 = ""
            elif isinstance(temp, str):
                lastName2 = temp
            else:
                lastName2 = ""

            try:
                fullName = name + ' ' + lastName1 + ' ' + lastName2
            except:
                fullName = ""

            # Gender
            temp = dataFrame[headers[19]][i]
            if isinstance(temp, str) and temp == 'Masculino':
                gender = 'MASCULINO'
            elif isinstance(temp, str) and temp == 'Femenino':
                gender = 'FEMENINO'

            # birthDate
            excel_birth_date = dataFrame[headers[17]][i]
            if isinstance(excel_birth_date, np.int64):
                birthDateNotUseful = datetime.date.fromordinal(
                    datetime.date(1900, 1, 1).toordinal() + excel_birth_date - 2)
                birthDate = birthDateNotUseful.strftime('%Y-%m-%d')
            if isinstance(excel_birth_date, datetime.date):
                birthDate = excel_birth_date.strftime('%Y-%m-%d')

            # address
            temp = dataFrame[headers[6]][i]
            if pd.isnull(temp):
                addressStreet = ""
            elif isinstance(temp, str):
                addressStreet = temp

            temp = dataFrame[headers[7]][i]
            if isinstance(temp, int):
                addressNumber = temp

            p04 = dataFrame[headers[24]][i]

            p05 = dataFrame[headers[25]][i]

            p06 = dataFrame[headers[26]][i]

            temp = dataFrame[headers[28]][i]
            if isinstance(temp, int) and temp == 1:
                palimento = True

            temp = dataFrame[headers[29]][i]
            if isinstance(temp, np.int64) and temp == 1:
                pagua = True

            temp = dataFrame[headers[30]][i]
            if isinstance(temp, np.int64) and temp == 1:
                psalud = True

            temp = dataFrame[headers[31]][i]
            if isinstance(temp, np.int64) and temp == 1:
                pcolchon = True

            temp = dataFrame[headers[32]][i]
            if isinstance(temp, np.int64) and temp == 1:
                pdiscapacidad = True

            temp = dataFrame[headers[38]][i]
            if isinstance(temp, np.int64) and temp == 1:
                phabitacional = True

            if addressStreet and addressNumber:

                # Geocoding
                bbox = [-71.61462052727242, -33.100438306264365, -71.57956428837826, -33.04425071807412]
                response = geocoder.forward(str(addressNumber) + ', ' + addressStreet, bbox=bbox,
                                            types=('address',))

                collection = response.json()

                if len(collection['features']) > 0:
                    counter += 1

                    longitude = collection['features'][0]['geometry']['coordinates'][0]
                    latitude = collection['features'][0]['geometry']['coordinates'][1]
                    coordinates = [longitude, latitude]

            temp = dataFrame[headers[11]][i]
            phone1 = temp

            data = {
                'informacionPersonal': {
                    'datosPersonales': {
                        'documento': {
                            'tipo': 'rut',
                            'numero': doc,
                            'digitoVerificador': digit
                        },
                        'nombre': name,
                        'apellido1': lastName1,
                        'apellido2': lastName2,
                        'fechaNacimiento': birthDate,
                        'genero': gender
                    },
                    'datosContacto': {
                        'direccion': {
                            'calle': addressStreet,
                            'numero': addressNumber,
                            'ciudad': city,
                            'pais': 'Chile',
                            'telefono1': phone1
                        }
                    },
                    'necesidadesDomiciliarias': {
                        'p04_vivienda_afectada': p04,
                        'p05_donde_duerme': p05,
                        'p06_enseres_afectados': p06,
                        'p09_nec_alimento': palimento,
                        'p09_nec_agua': pagua,
                        'p09_nec_salud': psalud,
                        'p09_nec_colcochone': pcolchon,
                        'p09_nec_discapacidad': pdiscapacidad,
                        'p09_nec_habitacional': phabitacional
                    },
                    'geometry':
                        {
                            'type': 'Point',
                            'coordinates': coordinates
                        },
                }
            }
            print(data)
            print('-----------------------')
            destinationCollection.insert_one(data)

print('located ', counter, 'of', totalCounter)
