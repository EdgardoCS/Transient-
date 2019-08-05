import os
import time
import pymongo
import pandas as pd
import numpy as np
from mapbox import Geocoder
from datetime import datetime

if __name__ == '__main__':
    myClient = pymongo.MongoClient("mongodb://localhost:27017/")

    myDB = myClient["individuals-valparaiso"]

    geocoder = Geocoder(
        access_token='pk.eyJ1IjoiZWRnYXJkb3MiLCJhIjoiY2o0OG54eDFjMGFjMzJxcGNlZzBnZnJrMiJ9.B__rQ4ztUAy6hXN7fjJHPw')

    myCollection = myDB["validated-cordillera-bbox"]

    ##
    # Cordillera

    currentFilePath = os.path.dirname(os.path.realpath(__file__))
    filePath = 'excels/validated/LISTA OFICIAL CESFAM CORDILLERA_ANA.xlsx'
    path = os.path.join(currentFilePath, filePath)

    dataFrame = pd.read_excel(path, sheet_name='reporte_pacientes_por_grupo_eta')

    headers = ['Nombre Paciente', 'NHC', 'Documento', 'Tipo doc', 'Fecha Nacimiento', 'Edad Actual', 'Fecha Cumpleaños',
               'Fecha Inscripción',
               'Sexo', 'Dirección', 'TELÉFONO 1', 'TELÉFONO 2', 'Sector', 'Estado', 'TELÉFONO 3', 'LAT', 'LON', 'DÍA 1',
               'DÍA 2', 'DÍA 3',
               'RESULTADO', 'ALUMNO']

    for i in range(0, len(dataFrame)):
        # If specifying latitude and longitude coordinates, list the longitude first and then latitude:

        doc = None
        docType = ''
        verifyingDigit = ''
        name = ''
        lastName1 = ''
        lastName2 = ''
        genre = ''
        birthDate = ''
        houseNumber = ''
        streetName = ''
        city = ''
        country = ''
        sector = None
        subSector = ''
        longitude = None
        latitude = None
        program = ''
        teamLead = ''
        status = ''
        observations = ''
        phone1 = None
        phone2 = None
        validated = ''

        # Document type
        temp = dataFrame[headers[3]][i]

        if isinstance(temp, str) and temp == 'R.U.T.':

            docType = 'rut'
            # Rut
            temp = dataFrame[headers[2]][i].replace(u'\xa0', u'')

            if isinstance(temp, str):
                tempRut = temp.split('-')
                doc = tempRut[0].strip()
                verifyingDigit = tempRut[1].strip()
            else:
                doc = str(temp)
                verifyingDigit = str(temp)

        # print(doc)

        # Name
        temp = dataFrame[headers[0]][i]
        if isinstance(temp, str):
            _temp = temp.split(' ')
            if len(_temp) == 1:
                name = _temp
            if len(_temp) == 2:
                name = _temp[0] + ' ' + _temp[1]
            if len(_temp) == 3:
                lastName1 = _temp[0]
                lastName2 = _temp[1]
                name = _temp[2]
            if len(_temp) == 4:
                name = _temp[2] + ' ' + _temp[3]
                lastName1 = _temp[0]
                lastName2 = _temp[1]
            if len(_temp) == 5:
                lastName1 = _temp[0]
                lastName2 = _temp[1]
                name = _temp[2] + ' ' + _temp[3] + ' ' + _temp[4]
            if len(_temp) == 6:
                lastName1 = _temp[0]
                lastName2 = _temp[1]
                name = _temp[2] + ' ' + _temp[3] + ' ' + _temp[4] + ' ' + _temp[5]

        # print(name, lastName1, lastName2)

        # Address
        temp = str(dataFrame[headers[9]][i])

        if isinstance(temp, str):
            tempAddress = temp.replace(u'\xa0', u'').split(',')

            if len(tempAddress) > 1:
                houseNumber = tempAddress[0].strip()
                streetName = tempAddress[1].strip()
                city = 'VALPARAISO'
                country = 'CHILE'

            else:
                houseNumber = temp.replace(u'\xa0', u'')
                streetName = temp.replace(u'\xa0', u'')
                city = 'VALPARAISO'
                country = 'CHILE'
        else:

            temp = str(dataFrame[headers[12]][i]).replace(u'\xa0', u'')

            houseNumber = temp.replace(u'\xa0', u'')
            streetName = temp.replace(u'\xa0', u'')
            city = 'VALPARAISO'
            country = 'CHILE'

        # Sector
        temp = str(dataFrame[headers[12]][i]).replace(u'\xa0', u' ').strip().split(' ')
        if len(temp) > 1:
            sector = temp[1]

        else:
            sector = temp

        # Longitude
        if pd.isnull(dataFrame[headers[16]][i]):
            longitude = None
        else:
            longitude = dataFrame[headers[16]][i]
        if pd.isnull(dataFrame[headers[15]][i]):
            latitude = None
        else:
            latitude = dataFrame[headers[15]][i]

        # print(latitude,longitude)

        temp = dataFrame[headers[20]][i]
        if temp == 'V' or temp == 'AA' or temp == 'AD' or temp == 'AT':
            validated = 'V'

        if temp == 'SD' or temp == 'NU' or temp == 'NUB' or temp == 'NO' or temp == 'NC':
            validated = 'NV'

        if temp == 'F':
            validated = 'F'

        if temp == 'CC':
            validated = 'CC'

        # sexo
        temp = str(dataFrame[headers[8]][i]).strip()

        if temp == 'Varón':
            genre = 'M'

        if temp == 'Mujer':
            genre = 'F'

        temp = dataFrame[headers[4]][i]
        try:
            _temp = datetime.fromordinal(datetime(1900, 1, 1).toordinal() + int(temp) - 2)
            birthDate = _temp.strftime('%Y-%m-%d')
        except:
            birthDate = '1900-01-01'

        if validated == 'V':

            # Phone
            temp = dataFrame[headers[10]][i]
            if isinstance(temp, int):
                phone1 = temp

            temp = dataFrame[headers[11]][i]
            if isinstance(temp, np.float64) and not pd.isnull(temp):
                phone2 = int(temp)

            # print(phone1, phone2)

            # Geocoding

            bboxCordillera = [-71.66031250127747, -33.063695783645244, -71.62231535369314, -33.02596835089963]

            response = geocoder.forward(houseNumber + ', ' + streetName, bbox=bboxCordillera, types=('address',))

            collection = response.json()

            # print(collection)

            if 'features' in collection and len(collection['features']) > 0:

                longitude = collection['features'][0]['geometry']['coordinates'][0]
                latitude = collection['features'][0]['geometry']['coordinates'][1]

            else:
                longitude = 0.0
                latitude = 0.0

        else:
            longitude = 0.0
            latitude = 0.0

            # Phone
            temp = dataFrame[headers[10]][i]
            if isinstance(temp, int):
                phone1 = temp

            temp = dataFrame[headers[11]][i]
            if isinstance(temp, np.float64) and not pd.isnull(temp):
                phone2 = int(temp)

        # print(birthDate)

        data = {
            'index': i,
            'datosPersonales': {
                'nombres': name,
                'apellido1': lastName1,
                'apellido2': lastName2,
                'genero': genre,
                'fechaNacimiento': birthDate

            },
            'documento': {
                'tipo': docType,
                'numero': doc,
                'digitoVerificador': verifyingDigit
            },
            'direccion': {
                'numero': houseNumber,
                'calle': streetName,
                'ciudad': city,
                'pais': country
            },
            'sector': sector,
            'geometry': {
                'type': 'Point',
                'coordinates': [longitude, latitude]
            },
            'telefonos': {
                'telefono1': phone1,
                'telefono2': phone2,
            },
            'resultadoValidacion': validated,
        }

        if validated == 'V':
            print(data)
            print('----------')

            myCollection.insert_one(data)

            time.sleep(0.33)
