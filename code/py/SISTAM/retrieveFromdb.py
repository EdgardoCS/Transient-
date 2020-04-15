import os
import math
import time
import pymongo
import datetime
import numpy as np
import pandas as pd
from pathlib import Path
from datetime import date
from dateutil.relativedelta import relativedelta

if __name__ == '__main__':

    counter = 0
    totalCounter = 0
    ##
    # Note: this script only works with pymongo 3.8
    client = pymongo.MongoClient("mongodb://localhost:27017/")

    db = client['demo']

    ##
    destinationCollection = db['personasContingencia']
    collection = db['personasContingencia']

    path = os.path.join(Path('/home/ed/Downloads/final-fonasa-avis.xlsx'))

    dataFrame = pd.read_excel(path, sheet_name='Sheet1')

    headers = dataFrame.columns

    counter = 0

    for i in range(0, len(dataFrame)):
        totalCounter += 1
        # for i in range(0, 100):
        # Initialize variables
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
        city = 'Valparaíso'
        cesfam = None
        relevance = None

        temp = dataFrame[headers[5]][i]  # .replace(u'\xa0', u'')

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
            # print('Rut: ' + str(doc) + '-' + digit)

            # Find patient using rut
            query = {'informacionPersonal.datosPersonales.documento.numero': doc}
            result = collection.find_one(query)
            if result is None:
                temp = dataFrame[headers[38]][i]
                if temp == 'V' and isinstance(temp, str):

                    counter += 1

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

                    # Gender
                    temp = dataFrame[headers[8]][i]
                    if pd.isnull(temp):
                        gender = ""
                    elif isinstance(temp, str) and temp == 'VARÓN':
                        gender = 'MASCULINO'
                    elif isinstance(temp, str) and temp == 'MUJER':
                        gender = 'FEMENINO'
                    else:
                        gender = ""
                    # print(gender, type(gender), 'should be str')

                    # birthDate
                    excel_birth_date = dataFrame[headers[6]][i]
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

                    # insurance
                    temp = dataFrame[headers[18]][i]
                    if pd.isnull(temp):
                        insurance = ""
                    elif isinstance(temp, str):
                        insurance = 'FONASA - ' + temp
                    # print(insurance, type(insurance), 'should be str')

                    # phone1
                    temp = dataFrame[headers[11]][i]
                    if pd.isnull(temp):
                        phone1 = None
                    elif isinstance(temp, int) and len(str(temp)) == 9:
                        phone1 = temp
                    else:
                        phone1 = None
                    # print(phone1, type(phone1), 'should  be int')

                    # phone2
                    temp = dataFrame[headers[12]][i]
                    if pd.isnull(temp):
                        phone2 = None
                    elif isinstance(temp, int) and len(str(temp)) == 9:
                        phone2 = temp
                    else:
                        phone2 = None
                    # print(phone2, type(phone2), 'should  be int')

                    # address
                    temp = dataFrame[headers[26]][i]
                    if pd.isnull(temp):
                        addressStreet = ""
                    elif isinstance(temp, str):
                        addressStreet = temp
                    else:
                        addressStreet = ""

                    temp = dataFrame[headers[30]][i]
                    if pd.isnull(temp):
                        addressNumber = None
                    elif isinstance(temp, int):
                        addressNumber = temp
                    else:
                        addressNumber = None

                    # temp = dataFrame[headers[9]][i]
                    # if pd.isnull(temp):
                    #     city = None
                    # elif isinstance(temp, str):
                    #     city = temp
                    # else:
                    #     city = ""
                    # print(city, type(str), 'should be str')

                    # cesfam
                    temp = dataFrame[headers[1]][i]
                    if pd.isnull(temp):
                        cesfam = ""
                    elif isinstance(temp, str):
                        cesfam = temp
                    else:
                        cesfam = ""
                    # print(cesfam, type(cesfam), 'should be str')

                    # admission date
                    excel_admission_date = dataFrame[headers[7]][i]
                    if pd.isnull(excel_admission_date):
                        admissionDate = '1900-01-01'
                    elif isinstance(excel_birth_date, str):
                        admissionDate = '1900-01-01'
                    try:
                        if isinstance(excel_admission_date, np.int64):
                            admissionDateNotUseful = datetime.date.fromordinal(
                                datetime.date(1900, 1, 1).toordinal() + excel_admission_date - 2)
                            admissionDate = admissionDateNotUseful.strftime('%Y-%m-%d')
                        if isinstance(excel_admission_date, datetime.date):
                            admissionDate = excel_admission_date.strftime('%Y-%m-%d')
                    except TypeError:
                        print('Error en el sujeto: ' + dataFrame[headers[3]][i] +
                              '. El formato de fecha es diferente al del resto del documento')
                    # print(admissionDate, type(admissionDate), 'should be str')

                    # coordinates
                    temp = dataFrame[headers[32]][i]
                    if pd.isnull(temp):
                        longitude = "longitude"
                    elif isinstance(temp, np.float64):
                        longitude = temp.item()
                    else:
                        longitude = "longitude"

                    temp = dataFrame[headers[33]][i]
                    if pd.isnull(temp):
                        latitude = "latitude"
                    elif isinstance(temp, np.float64):
                        latitude = temp.item()
                    else:
                        latitude = "latitude"
                    coordinates = [longitude, latitude]
                    # print(coordinates)

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
                                    'ciudad': 'Valparaíso',
                                    'pais': 'Chile',
                                    'telefono1': phone1,
                                    'telefono2': phone2
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
                            'prodecenciaData': {
                                'fuente': 'Fonasa',
                                'fecha': 'Diciembre2019'
                            },
                            'geometry':
                                {
                                    'type': 'Point',
                                    'coordinates': coordinates
                                }
                        }
                    }
                    # print(data)

                    print('inserted ', counter, 'of', totalCounter)
                    destinationCollection.insert_one(data)
                else:
                    print('relevance below 0.5')
            else:
                print('user already exists')

print('-----------------------')
print('success')
