import os
import pymongo
import pandas as pd
from mapbox import Geocoder
from datetime import datetime
import time

if __name__ == '__main__':

    myClient = pymongo.MongoClient("mongodb://localhost:27017/")

    myDB = myClient["individuals-valparaiso"]

    geocoder = Geocoder(
        access_token='pk.eyJ1IjoiZWRnYXJkb3MiLCJhIjoiY2o0OG54eDFjMGFjMzJxcGNlZzBnZnJrMiJ9.B__rQ4ztUAy6hXN7fjJHPw')

    ##
    # Rodelillo

    myCollection = myDB["validated-rodelillo-bbox"]

    currentFilePath = os.path.dirname(os.path.realpath(__file__))
    filePath = 'excels/validated/validated-rodelillo.xlsx'
    path = os.path.join(currentFilePath, filePath)

    dataFrame = pd.read_excel(path, sheet_name='Hoja2')

    headers = ['Nombre Paciente', 'NHC', 'Documento', 'Tipo doc', 'Fecha Nacimiento', 'Edad Actual', 'Fecha Cumpleaños',
               'Fecha Inscripción', 'Sexo', 'Dirección', 'Teléfono 1', 'Sector', 'Estado',
               'Teléfono 2', 'Día 1', 'Día 2', 'Día 3', 'Resultado', 'Estudiante',
               ]

    for i in range(0, len(dataFrame)):
    #for i in range(0,20):
        # print(i)

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

            temp = str(dataFrame[headers[7]][i]).replace(u'\xa0', u'')

            houseNumber = temp.replace(u'\xa0', u'')
            streetName = temp.replace(u'\xa0', u'')
            city = 'VALPARAISO'
            country = 'CHILE'
        # print(houseNumber, streetName)

        # Sector
        temp = dataFrame[headers[11]][i]
        if isinstance(temp, str):
            _temp = temp.split(' ')
            if len(_temp) == 1:
                sector = _temp[0]
            elif len(_temp) == 2:
                sector = _temp[1]
        # print(sector)

        # Validated
        temp = str(dataFrame[headers[17]][i])

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

        temp = dataFrame[headers[4]][i]

        if isinstance(temp, str):
            birthDate = temp
            # birthDate = datetime.fromordinal(datetime(1900, 1, 1).toordinal() + int(temp) - 2)
            # print(birthDate)

        if validated == 'V':

            if temp != 'nan' and temp != '':

                # Phone1
                temp = dataFrame[headers[10]][i]
                if isinstance(temp, int):
                    phone1 = temp
                else:
                    temp = str(temp)
                    if temp != 'nan' and temp[1] == ' ' or temp[2] == ' ':
                        _temp = temp.split(' ')
                        phone1 = _temp[0] + _temp[1]
                    if temp != 'nan' and temp[1] == '-' or temp[2] == '-':
                        _temp = temp.split('-')
                        _temp2 = _temp[1].split(' ')
                        phone1 = _temp[0] + _temp2[0]
                # print(phone1)
                if isinstance(temp, str):
                    if temp != 'nan' and len(temp) > 15:
                        _temp = temp.split(' ')
                        try:
                            _temp2 = _temp[1].split('-')
                            phone2 = _temp2[0] + _temp2[1]
                        except:
                            _temp2 = _temp[1].split('/')
                            if len(_temp2) == 2:
                                phone2 = _temp2[1]

                # Phone2
                temp = dataFrame[headers[13]][i]
                if isinstance(temp, int):
                    phone2 = temp
                else:
                    temp = str(temp)
                    if temp != 'nan' and temp[0] == ' ':
                        _temp = temp.split(' ')
                        if len(_temp) == 3 or len(_temp) == 4:
                            phone2 = _temp[1] + _temp[2]
                            # print(phone2)
                        else:
                            _temp2 = _temp[1].split('-')
                            phone2 = _temp2[0] + _temp2[1]

                # print(phone1, phone2)

                # Geocoding
                '''
                bboxRodelillo = [-71.61056248082001, -33.0685778274808, -71.55293279398813, -33.03733118802327]

                response = geocoder.forward(houseNumber + ', ' + streetName, bbox=bboxRodelillo, types=('address',))

                collection = response.json()

                if 'features' in collection and len(collection['features']) > 0:
                    longitude = collection['features'][0]['geometry']['coordinates'][0]
                    latitude = collection['features'][0]['geometry']['coordinates'][1]
                else:
                    longitude = 0.0
                    latitude = 0.0

            else:
                longitude = 0.0
                latitude = 0.0

                temp = dataFrame[headers[10]][i]
                if isinstance(temp, int):
                    phone1 = temp
                else:
                    temp = str(temp)
                    if temp != 'nan' and temp[1] == ' ' or temp[2] == ' ':
                        _temp = temp.split(' ')
                        phone1 = _temp[0] + _temp[1]
                    if temp != 'nan' and temp[1] == '-' or temp[2] == '-':
                        _temp = temp.split('-')
                        _temp2 = _temp[1].split(' ')
                        phone1 = _temp[0] + _temp2[0]
                # print(phone1)
                if isinstance(temp, str):
                    if temp != 'nan' and len(temp) > 15:
                        _temp = temp.split(' ')
                        try:
                            _temp2 = _temp[1].split('-')
                            phone2 = _temp2[0] + _temp2[1]
                        except:
                            _temp2 = _temp[1].split('/')
                            if len(_temp2) == 2:
                                phone2 = _temp2[1]

                # Phone2
                temp = dataFrame[headers[13]][i]
                if isinstance(temp, int):
                    phone2 = temp
                else:
                    temp = str(temp)
                    if temp != 'nan' and temp[0] == ' ':
                        _temp = temp.split(' ')
                        if len(_temp) == 3 or len(_temp) == 4:
                            phone2 = _temp[1] + _temp[2]
                            # print(phone2)
                        else:
                            _temp2 = _temp[1].split('-')
                            phone2 = _temp2[0] + _temp2[1]

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
