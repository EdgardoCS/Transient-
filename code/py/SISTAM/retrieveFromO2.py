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
    ##
    # Note: this script only works with pymongo 3.8
    client = pymongo.MongoClient("mongodb://localhost:27017/")

    db = client['demo']

    ##
    # MenaDb
    destinationCollection = db['oxigenoDependientes']
    collection = db['personasContingencia']

    path = os.path.join(Path('/home/ed/Downloads/OXIGENOS DEPENDIENTES CORMUVAL.xlsx'))

    dataFrame = pd.read_excel(path, sheet_name='Hoja1')

    headers = dataFrame.columns

    counter = 0

    for i in range(0, len(dataFrame)):

        # Initialize variables
        # o2 data
        doc = None
        digit = None
        name = None
        lastName1 = None
        lastName2 = None
        gender = None
        birthDate = '1900-01-01'
        insurance = None
        phone = None
        address = None
        city = None
        cesfam = None
        admissionDate = '1900-01-01'
        admissionAgeYears = None
        admissionAgeMonths = None
        currentAgeYears = None
        currentAgeMonths = None
        servicioSalud = None
        hospitalDerivation = None
        hospitalControl = None
        program = None
        ges = None
        diagnosis = None
        associatedPathology = None
        nutritionalStatus = None
        bronquiectasias = None
        status = None
        equipment = None
        oxygen = None
        useHours = None

        temp = dataFrame[headers[0]][i]  # .replace(u'\xa0', u'')

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
        # print('Rut: ' + str(doc) + '-' + digit)

        # Find patient using rut
        query = {'informacionPersonal.datosPersonales.documento.numero': doc}
        result = collection.find_one(query)
        # print(result)

        # Name
        temp = dataFrame[headers[1]][i]
        if pd.isnull(temp):
            name = None
        elif isinstance(temp, str):
            name = temp

        # lastName
        temp = dataFrame[headers[2]][i]
        if pd.isnull(temp):
            lastName1 = None
        elif isinstance(temp, str):
            lastName1 = temp

        temp = dataFrame[headers[3]][i]
        if pd.isnull(temp):
            lastName2 = None
        elif isinstance(temp, str):
            lastName2 = temp
        try:
            fullName = name + ' ' + lastName1 + ' ' + lastName2
        except:
            fullName = None
        # print(fullName, type(fullName), 'should be str')

        # Gender
        temp = dataFrame[headers[4]][i]
        if pd.isnull(temp):
            gender = None
        if isinstance(temp, str) and temp == 'Masculino':
            gender = 'MASCULINO'
        if isinstance(temp, str) and temp == 'Femenino':
            gender = 'FEMENINO'
        # print(gender, type(gender), 'should be str')

        # birthDate
        excel_birth_date = dataFrame[headers[5]][i]
        if pd.isnull(excel_birth_date):
            excel_birth_date = '1900-01-01'
        elif isinstance(excel_birth_date, str):
            excel_birth_date = '1900-01-01'
        try:
            if isinstance(excel_birth_date, int):
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
        temp = dataFrame[headers[6]][i]
        if pd.isnull(temp):
            insurance = None
        elif isinstance(temp, str):
            insurance = temp
        # print(insurance, type(insurance), 'should be str')

        # phone
        temp = dataFrame[headers[7]][i]
        if pd.isnull(temp):
            phone = None
        elif isinstance(temp, int):
            phone = temp
        else:
            phone = None
        # print(phone, type(phone), 'should  be int')

        # address

        # city
        temp = dataFrame[headers[9]][i]
        if pd.isnull(temp):
            city = None
        elif isinstance(temp, str):
            city = temp
        else:
            city = None
        # print(city, type(str), 'should be str')

        # cesfam
        temp = dataFrame[headers[10]][i]
        if pd.isnull(temp):
            cesfam = None
        elif isinstance(temp, str):
            cesfam = temp
        else:
            cesfam = None
        # print(cesfam, type(cesfam), 'should be str')

        # admission date
        excel_admission_date = dataFrame[headers[11]][i]
        if pd.isnull(excel_admission_date):
            admissionDate = '1900-01-01'
        elif isinstance(excel_birth_date, str):
            admissionDate = '1900-01-01'
        try:
            if isinstance(excel_admission_date, int):
                admissionDateNotUseful = datetime.date.fromordinal(
                    datetime.date(1900, 1, 1).toordinal() + excel_admission_date - 2)
                admissionDate = admissionDateNotUseful.strftime('%Y-%m-%d')
            if isinstance(excel_admission_date, datetime.date):
                admissionDate = excel_admission_date.strftime('%Y-%m-%d')
        except TypeError:
            print('Error en el sujeto: ' + dataFrame[headers[3]][i] +
                  '. El formato de fecha es diferente al del resto del documento')
        # print(admissionDate, type(admissionDate), 'should be str')

        # admissionAgeYears
        temp = dataFrame[headers[13]][i]
        if pd.isnull(temp):
            admissionAgeYears = None
        elif isinstance(temp, np.int64):
            admissionAgeYears = temp.item()
        else:
            admissionAgeYears = None

        # admissionAgeMonths
        temp = dataFrame[headers[14]][i]
        if pd.isnull(temp):
            admissionAgeMonths = None
        elif isinstance(temp, np.int64):
            admissionAgeMonths = temp.item()
        else:
            admissionAgeMonths = None
        # print('admissionAge', admissionAgeYears, 'years', admissionAgeMonths, 'months')

        # currentAgeYears
        temp = dataFrame[headers[15]][i]
        if pd.isnull(temp):
            currentAgeYears = None
        elif isinstance(temp, np.int64):
            currentAgeYears = temp.item()
        else:
            currentAgeYears = None

        # currentAgeMonths
        temp = dataFrame[headers[16]][i]
        if pd.isnull(temp):
            currentAgeMonths = None
        elif isinstance(temp, np.int64):
            currentAgeMonths = temp.item()
        else:
            currentAgeMonths = None
        # print('currentAge', currentAgeYears, 'years', currentAgeMonths, 'months')

        # servicioSalud
        temp = dataFrame[headers[17]][i]
        if pd.isnull(temp):
            servicioSalud = None
        elif isinstance(temp, str):
            servicioSalud = temp
        else:
            servicioSalud = None
        # print(servicioSalud, type(servicioSalud), 'should be str')

        # hospitalDerivation
        temp = dataFrame[headers[18]][i]
        if pd.isnull(temp):
            hospitalDerivation = None
        elif isinstance(temp, str):
            hospitalDerivation = temp
        else:
            hospitalDerivation = None
        # print(hospitalDerivation, type(hospitalDerivation), 'should be str')

        # hospitalControl
        temp = dataFrame[headers[19]][i]
        if pd.isnull(temp):
            hospitalControl = None
        elif isinstance(temp, str):
            hospitalControl = temp
        else:
            hospitalControl = None
        # print(hospitalControl, type(hospitalControl), 'should be str')

        # program
        temp = dataFrame[headers[20]][i]
        if pd.isnull(temp):
            program = None
        elif isinstance(temp, str):
            program = temp
        else:
            program = None
        # print(program, type(program), 'should be str')

        # ges
        temp = dataFrame[headers[21]][i]
        if pd.isnull(temp):
            ges = None
        elif isinstance(temp, str):
            ges = temp
        else:
            ges = None
        # print(ges, type(ges), 'should be str')

        # diagnosis
        temp = dataFrame[headers[22]][i]
        if pd.isnull(temp):
            diagnosis = None
        elif isinstance(temp, str):
            diagnosis = temp
        else:
            diagnosis = None
        # print(diagnosis, type(diagnosis), 'should be str')

        # associatedPathology
        temp = dataFrame[headers[23]][i]
        if pd.isnull(temp):
            associatedPathology = None
        elif isinstance(temp, str):
            associatedPathology = temp
        else:
            associatedPathology = None
        # print(associatedPathology, type(associatedPathology), 'should be str')

        # nutritionalStatus
        temp = dataFrame[headers[24]][i]
        if pd.isnull(temp):
            nutritionalStatus = None
        elif isinstance(temp, str):
            nutritionalStatus = temp
        else:
            nutritionalStatus = None
        # print(nutritionalStatus, type(nutritionalStatus), 'should be str')

        # bronquiectasias
        temp = dataFrame[headers[25]][i]
        if pd.isnull(temp):
            bronquiectasias = None
        elif isinstance(temp, str):
            bronquiectasias = temp
        else:
            bronquiectasias = None
        # print(bronquiectasias, type(bronquiectasias), 'should be str')

        # status
        temp = dataFrame[headers[26]][i]
        if pd.isnull(temp):
            status = None
        elif isinstance(temp, str):
            status = temp
        else:
            status = None
        # print(status, type(status), 'should be str')

        # equipment
        temp = dataFrame[headers[27]][i]
        if pd.isnull(temp):
            equipment = None
        elif isinstance(temp, str):
            equipment = temp
        else:
            equipment = None
        # print(equipment, type(equipment), 'should be str')

        # oxygen
        temp = dataFrame[headers[28]][i]
        if pd.isnull(temp):
            oxygen = None
        elif isinstance(temp, np.float64):
            oxygen = temp.item()
        else:
            oxygen = None
        # print(oxygen, type(oxygen), 'should be float')

        # useHours
        temp = dataFrame[headers[29]][i]
        if pd.isnull(temp):
            useHours = None
        elif isinstance(temp, np.float64):
            useHours = temp.item()
        else:
            useHours = None
        # print(useHours, type(useHours), 'should be float')

        data = {
            'datosPersonales': {
                'rut': {
                    'numero': doc,
                    'digitoVerificador': digit
                },
                'nombreCompleto': fullName,
                'sexo': gender,
                'fechaNacimiento': birthDate,
                'dirección': None,
                'telefono': phone,
                'aseguradora': insurance,
                'servicioSalud': servicioSalud,
                'cesfam': cesfam

            },
            'tipoPrestación': 'oxigenoDependientes',
            'infoPrestación': {
                'fechaIngreso': admissionDate,
                'hospitalControl': hospitalControl,
                'program': program,
                'ges': ges,
                'diagnostico': diagnosis,
                'patologíaAsociada': associatedPathology,
                'estadoNutricional': nutritionalStatus,
                'estadoTratamiento': status,
                'bronquiectasias': bronquiectasias,
                'equipamiento': equipment,
                'nivelOxigeno': oxygen,
                'horasDeUso': useHours
            }
        }
        print(data)
        print('-----------------------')

        destinationCollection.insert_one(data)

        print('success')
