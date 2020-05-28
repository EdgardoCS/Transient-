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

"""
notas. 
1. Identificar procedencia de datos -> comuna - centro de salud
2. Cambiar variables None a False
3. Agregar campo/objeto institución

"""

if __name__ == '__main__':

    counter = 0
    totalCounter = 0
    ##
    # Note: this script only works with pymongo 3.8
    client = pymongo.MongoClient("mongodb://localhost:27017/")

    db = client['demo']

    ##
    destinationCollection = db['personasContingencia']

    path = os.path.join(Path('/home/ed/Downloads/loncoche_geo(1).xlsx'))

    dataFrame = pd.read_excel(path, sheet_name='D.S.M. LONCOCHE')

    headers = dataFrame.columns

    counter = 0

    geocoder = Geocoder(
        access_token='pk.eyJ1IjoiZWRnYXJkb3MiLCJhIjoiY2o0OG54eDFjMGFjMzJxcGNlZzBnZnJrMiJ9.B__rQ4ztUAy6hXN7fjJHPw')

    # print(sheets)

    longitude = None  # AA
    latitude = None  # AB

    for i in range(0, len(dataFrame)):
        totalCounter += 1

        # xlsx data

        doc = None
        digit = None
        name = None
        lastName1 = None
        lastName2 = None
        gender = None
        birthDate = '1900-01-01'
        admissionDate = '1900-01-01'
        insurance = None
        phone1 = None
        phone2 = None
        address = None
        city = 'Loncoche'
        cesfam = None
        relevance = None
        coordinates = [0.0, 0.0]

        temp = dataFrame[headers[1]][i]  # .replace(u'\xa0', u'')

        if isinstance(temp, str):
            tempRut = temp.split('-')

            if len(tempRut) > 1:
                docType = 'rut'
                doc = tempRut[0].strip()
                digit = tempRut[1].strip()
            else:
                docType = 'other'
                doc = temp
                digit = temp
        else:
            docType = 'other'
            doc = None
            digit = None

        if doc is not None:

            # Name
            temp = dataFrame[headers[2]][i]
            if pd.isnull(temp):
                name = ""
            elif isinstance(temp, str):
                name = temp
            else:
                name = ""

            # lastName
            temp = dataFrame[headers[3]][i]
            if pd.isnull(temp):
                lastName1 = ""
            elif isinstance(temp, str):
                lastName1 = temp
            else:
                lastName1 = ""

            temp = dataFrame[headers[4]][i]
            if pd.isnull(temp):
                lastName2 = ""
            elif isinstance(temp, str):
                lastName2 = temp
            else:
                lastName2 = ""

            try:
                fullName = name + ' ' + lastName1 + ' ' + lastName2
            except:
                fullName = None
            # print(fullName, type(fullName), 'should be str')
            if fullName is not None:

                # Gender
                temp = dataFrame[headers[6]][i]
                if pd.isnull(temp):
                    gender = ""
                elif isinstance(temp, str) and temp == 'M':
                    gender = 'MASCULINO'
                elif isinstance(temp, str) and temp == 'F':
                    gender = 'FEMENINO'
                else:
                    gender = ""
                # print(gender, type(gender), 'should be str')

                # birthDate
                excel_birth_date = dataFrame[headers[5]][i]
                if pd.isnull(excel_birth_date):
                    excel_birth_date = '1900-01-01'
                elif isinstance(excel_birth_date, str):
                    excel_birth_date = '1900-01-01'
                try:
                    if isinstance(excel_birth_date, np.int64):
                        birthDateNotUseful = datetime.date.fromordinal(
                            datetime.date(1900, 1, 1).toordinal() + excel_birth_date - 2)
                        birthDate = birthDateNotUseful.strftime('%Y-%m-%d')
                    if isinstance(excel_birth_date, datetime.date):
                        birthDate = excel_birth_date.strftime('%Y-%m-%d')
                except TypeError as e:
                    print(e)
                    print('Error en el sujeto: ' + dataFrame[headers[3]][i] +
                          '. El formato de fecha de nacimiento es diferente al del resto del documento')
                    print('Tipo de dato: ' + str(type(excel_birth_date)))
                # print(birthDate, type(birthDate), 'should be str')

                # cesfam
                temp = dataFrame[headers[12]][i]
                if pd.isnull(temp):
                    cesfam = None
                elif isinstance(temp, str):
                    cesfam = temp
                else:
                    cesfam = None
                # print(cesfam, type(cesfam), 'should be str')

                # address
                temp = dataFrame[headers[8]][i]
                if pd.isnull(temp):
                    addressStreet = ""
                elif isinstance(temp, str):
                    addressStreet = temp
                else:
                    addressStreet = ""

                temp = dataFrame[headers[9]][i]
                if pd.isnull(temp):
                    addressNumber = None
                elif isinstance(temp, int):
                    addressNumber = temp
                else:
                    addressNumber = None

                if addressStreet is not None and addressNumber is not None:

                    # Geocoding
                    bbox = [-72.9017885221082, -39.5096176823395, -72.2996077573355, -39.2148627951642]  # loncoche

                    response = geocoder.forward(str(addressNumber) + ', ' + addressStreet, bbox=bbox,
                                                types=('address',))

                    collection = response.json()

                    # print('i: ' + str(i))
                    # print(collection)

                    if len(collection['features']) > 0:

                        counter += 1
                        # print(collection['features'])
                        # print(collection['features'][0])
                        # print(collection['features'][0]['geometry'])
                        # print(collection['features'][0]['geometry']['coordinates'])

                        longitude = collection['features'][0]['geometry']['coordinates'][0]
                        latitude = collection['features'][0]['geometry']['coordinates'][1]
                        coordinates = [longitude, latitude]


                    else:
                        longitude = 0.0
                        latitude = 0.0
                        coordinates = [longitude, latitude]

                        # print('Street: ' + str(addressStreet))
                        # print('Number: ' + str(addressNumber))
                        # print('Longitude: ' + str(longitude))
                        # print('Latitude: ' + str(latitude))
                        # print('**********')

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
                                'block': "",
                                'ciudad': 'Loncoche',
                                'pais': 'Chile',
                                'telefono1': "",
                                'telefono2': ""
                            }
                        },
                        'informacionFamiliar': {
                            'cesfam': cesfam,
                            'viveSolo': None,
                            'movilidad': None,
                            'gradoDependencia': None,
                            'tieneCuidador': None,
                            'cuidador': {
                                'nombre': None,
                                'apellido1': None,
                                'apellido2': None,
                                'telefono': None,
                                'viveConLaPersona': None,
                                'remunerado': None
                            }
                        },
                        'necesidadesDomiciliarias': {
                            'pacam': None,
                            'farmacia': None,
                            'pni': None,
                            'sarsCov': None,
                        },
                        'vacuna': False,
                        'covid': False,
                        'geometry':
                            {
                                'type': 'Point',
                                'coordinates': coordinates
                            },
                        "cronico_respiratorio": False
                    },
                    "institucion": {
                        "loncoche": True
                    }
                }
                print(data)
                print('-----------------------')
                destinationCollection.insert_one(data)

print('located ', counter, 'of', totalCounter)
