import os
import time
import pymongo
import pandas as pd
from mapbox import Geocoder
from datetime import datetime

if __name__ == '__main__':

    myClient = pymongo.MongoClient("mongodb://localhost:27017/")

    myDB = myClient["individuals-valparaiso"]

    geocoder = Geocoder(
        access_token='pk.eyJ1IjoiZWRnYXJkb3MiLCJhIjoiY2o0OG54eDFjMGFjMzJxcGNlZzBnZnJrMiJ9.B__rQ4ztUAy6hXN7fjJHPw')

    ##
    # Padre Damián

    myCollection = myDB["validated-padre-damian-bbox"]

    currentFilePath = os.path.dirname(os.path.realpath(__file__))
    filePath = 'excels/validated/LISTA OFICIAL CESFAM PADRE DAMIAN_anto_tel.3.xlsx'
    path = os.path.join(currentFilePath, filePath)

    dataFrame = pd.read_excel(path, sheet_name='LISTA OFICIAL CESFAM PADRE DAMI')

    headers = ['Nombre Paciente', 'Doc', 'Tipo Doc', 'Fecha Nacimiento', 'Edad', 'Fecha Inscripción', 'Sexo',
               'Dirección', 'Teléfono 1', 'Sector', 'Estado', 'Teléfono 2', 'Teléfono 3',
               'lat', 'long', 'Día 1', 'Día 2', 'Día 3', 'Resultado', 'Estudiante',
               ]

    for i in range(0, len(dataFrame)):
        # print(i)
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
        temp = dataFrame[headers[2]][i]

        if isinstance(temp, str) and temp == 'R.U.T.':
            docType = 'rut'

            # Rut
            temp = dataFrame[headers[1]][i].replace(u'\xa0', u'')

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
                name = _temp[0]
            if len(_temp) == 2:
                name = _temp[1]
                lastName1 = _temp[0]
            if len(_temp) == 3:
                name = _temp[2]
                lastName1 = _temp[0]
                lastName2 = _temp[1]
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
        # print(lastName1, lastName2, name)

        # Address

        temp = str(dataFrame[headers[7]][i])

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

            temp = str(dataFrame[headers[7]][i]).replace(u'\xa0', u'')

            houseNumber = temp.replace(u'\xa0', u'')
            streetName = temp.replace(u'\xa0', u'')
            city = 'VALPARAISO'
            country = 'CHILE'

        # Sector
        temp = dataFrame[headers[9]][i]
        if isinstance(temp, str):
            _temp = temp.split(' ')
            if len(_temp) == 1:
                sector = _temp[0]
            elif len(_temp) == 2:
                sector = _temp[1]
        # print(sector)

        # Longitude
        longitude = dataFrame[headers[15]][i]

        # Latitude
        latitude = dataFrame[headers[14]][i]

        # print(latitude, longitude)

        # Validated
        temp = str(dataFrame[headers[18]][i])

        if temp == 'V' or temp == 'AA' or temp == 'AD' or temp == 'AT':
            validated = 'V'

        if temp == 'SD' or temp == 'NU' or temp == 'NUB' or temp == 'NO' or temp == 'NC':
            validated = 'NV'

        if temp == 'F':
            validated = 'F'

        if temp == 'CC':
            validated = 'CC'

        temp = str(dataFrame[headers[6]][i])
        if temp == 'Varón':
            genre = 'M'

        if temp == 'Mujer':
            genre = 'F'

        temp = dataFrame[headers[3]][i]

        if isinstance(temp, int):
            _temp = datetime.fromordinal(datetime(1900, 1, 1).toordinal() + temp - 2)
            birthDate = _temp.strftime('%Y-%m-%d')

        # print(validated)

        if validated == 'V':
            # Phone1
            temp = str(dataFrame[headers[8]][i])

            if temp != 'nan' and temp != '':
                try:
                    phone1 = int(str(dataFrame[headers[8]][i]).strip().replace(u'\xa0', u''))

                except ValueError:
                    print(ValueError)

            else:
                phone1 = None

            # Phone2
            temp = str(dataFrame[headers[11]][i])

            if temp != 'nan' and temp != '':
                try:
                    phone2 = int(str(dataFrame[headers[11]][i]).strip().replace(u'\xa0', u''))
                except ValueError:
                    print(ValueError)
            else:
                phone2 = None

            # Geocoding
            '''
            bboxPadreDamian = [-71.60609040699032, -33.067201824969445, -71.52849574615635, -33.02087998383863]

            response = geocoder.forward(houseNumber + ', ' + streetName, bbox=bboxPadreDamian, types=('address',))

            collection = response.json()

            # print(collection)

            if len(collection['features']) > 0:

                longitude = collection['features'][0]['geometry']['coordinates'][0]
                latitude = collection['features'][0]['geometry']['coordinates'][1]

            else:
                longitude = 0.0
                latitude = 0.0

        else:
            longitude = 0.0
            latitude = 0.0

            # Phone1
            # Phone1
            temp = str(dataFrame[headers[8]][i])

            if temp != 'nan' and temp != '':
                try:
                    phone1 = int(str(dataFrame[headers[8]][i]).strip().replace(u'\xa0', u''))

                except ValueError:
                    print(ValueError)

            else:
                phone1 = None

            # Phone2
            temp = str(dataFrame[headers[11]][i])

            if temp != 'nan' and temp != '':
                try:
                    phone2 = int(str(dataFrame[headers[11]][i]).strip().replace(u'\xa0', u''))
                except ValueError:
                    print(ValueError)
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
            '''
        time.sleep(0.33)
