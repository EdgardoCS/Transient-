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

    myCollection = myDB["validated-puertas-negras-bbox"]

    ##
    # Puertas Negras

    currentFilePath = os.path.dirname(os.path.realpath(__file__))
    filePath = 'excels/validated/LISTA OFICIAL CESFAM PUERTAS NEGRAS.xlsx'
    path = os.path.join(currentFilePath, filePath)

    dataFrame = pd.read_excel(path, sheet_name='reporte_detalle_pacientes_incri')

    headers = ['Centro',
               'C Familia',
               'NHC',
               'Nombre',
               'A Paterno',
               'A Materno',
               'N Social',
               'Doc',
               'Tipo doc',
               'Fecha Nac',
               'Edad',
               'Fecha Inscrip ',
               'Sexo',
               'Etnia',
               'Población',
               'Dirección',
               'Sector',
               'U Vecinal',
               'Telf 1',
               'Telf 2',
               'Previsión',
               'Email',
               'Nacionalidad',
               'Legajo',
               'Estado',
               'Día 1',
               'Día 2',
               'Día 3',
               'Resultado',
               'Estudiante'
               ]

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
        temp = dataFrame[headers[8]][i]

        if isinstance(temp, str) and temp == 'R.U.T.':

            docType = 'rut'
            # Rut
            temp = dataFrame[headers[7]][i].replace(u'\xa0', u'')

            if isinstance(temp, str):
                tempRut = temp.split('-')
                doc = tempRut[0].strip()
                verifyingDigit = tempRut[1].strip()
            else:
                doc = str(temp)
                verifyingDigit = str(temp)

        # Name
        temp = dataFrame[headers[3]][i]
        if isinstance(temp, str):
            _temp = temp.split(' ')
            if len(_temp) == 1:
                name = _temp[0]
            if len(_temp) == 2:
                name = _temp[0] + ' ' + _temp[1]
            if len(_temp) == 3:
                name = _temp[0] + ' ' + _temp[1] + ' ' + _temp[2]
            if len(_temp) == 4:
                name = _temp[0] + ' ' + _temp[1] + ' ' + _temp[2] + ' ' + _temp[3]

        temp = dataFrame[headers[4]][i]
        if isinstance(temp, str):
            lastName1 = temp

        temp = dataFrame[headers[5]][i]
        if isinstance(temp, str):
            lastName2 = temp

        # Address
        temp = str(dataFrame[headers[15]][i])

        if isinstance(temp, str):
            if ',' in temp:
                tempAddress = temp.replace(u'\xa0', u'').split(',')
                houseNumber = tempAddress[0].strip()
                _temp = tempAddress[1]
                if '(CÁRCEL)' in _temp:
                    __temp = _temp.split('(CÁRCEL)')
                    streetName = __temp[0]
                else:
                    streetName = tempAddress[1].strip()
                city = 'VALPARAISO'
                country = 'CHILE'

        # Sector
        temp = str(dataFrame[headers[16]][i]).replace(u'\xa0', u' ').strip().split(' ')
        if len(temp) > 1:
            sector = temp[1]
        else:
            sector = temp[0]

        temp = dataFrame[headers[28]][i]
        if temp == 'V' or temp == 'AA' or temp == 'AD' or temp == 'AT':
            validated = 'V'

        if temp == 'SD' or temp == 'NU' or temp == 'NUB' or temp == 'NO' or temp == 'NC':
            validated = 'NV'

        if temp == 'F':
            validated = 'F'

        if temp == 'CC':
            validated = 'CC'

        # sexo
        temp = str(dataFrame[headers[12]][i]).strip()

        if temp == 'VARÓN':
            genre = 'M'

        if temp == 'MUJER':
            genre = 'F'

        temp = dataFrame[headers[9]][i]
        try:
            _temp = datetime.fromordinal(datetime(1900, 1, 1).toordinal() + int(temp) - 2)
            birthDate = _temp.strftime('%Y-%m-%d')
        except:
            birthDate = '1900-01-01'

        if validated == 'V':

            # print(doc, name, lastName1, lastName2, ',', houseNumber, streetName, sector, ',', genre)

            # Phone
            temp = dataFrame[headers[18]][i]

            if isinstance(temp, int):
                phone1 = temp
            elif isinstance(temp, str):
                phone1 = int(temp)
            temp = dataFrame[headers[19]][i]
            if isinstance(temp, str) and not pd.isnull(temp):
                if '\xa0' in temp:
                    _temp = temp.split('\xa0')
                    phone2 = _temp[0] + _temp[1]
                    if len(phone2) < 9 and len(phone2) > 1:
                        phone2 = str(9) + phone2
                else:
                    phone2 = int(temp)
            if isinstance(temp, int) and not pd.isnull(temp):
                phone2 = temp
            try:
                phone2 = int(phone2)
            except:
                phone2 = None

            #Geocoding

            bboxpuertasnegras = [-71.65295505947964, -33.064975348855754, -71.63306720478008, -33.0482229306695]

            response = geocoder.forward(houseNumber + ', ' + streetName, bbox=bboxpuertasnegras, types=('address',))

            collection = response.json()

            print(collection)

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
            temp = dataFrame[headers[18]][i]
            if isinstance(temp, int):
                phone1 = temp
            if isinstance(temp, str):
                if '\xa0' in temp:
                    _temp = temp.split('\xa0')
                    if _temp[0] == '9' or _temp[0] == '32':
                        phone1 = _temp[0] + _temp[1]
                    else:
                        try:
                            phone1 = int(_temp[1])
                        except:
                            phone1 = None

            temp = dataFrame[headers[19]][i]
            if isinstance(temp, int):
                phone2 = temp
            if isinstance(temp, str):
                if '\xa0' in temp:
                    if '-' in temp:
                        _temp = temp.split('-')
                        phone2 = int(_temp[0] + _temp[1])
                    else:
                        phone2 = None

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
