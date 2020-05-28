import pandas as pd
import numpy as np
import pymongo
import datetime
import math

import os
import time

if __name__ == '__main__':

    ##
    # Note: this script only works with pymongo 3.8
    client = pymongo.MongoClient("mongodb://localhost:27017/")

    db = client['individuals-valparaiso']

    ##
    # Rodelillo DB

    collection = db['validated-rodelillo-bbox']

    destinationCollection = db["pscv-rodelillo"]

    path = os.path.join(os.path.dirname(os.path.realpath(__file__)),'excels/tarjetero/rodelillo/Programa de Cardio Sector B 2019.xlsm')
    #path = os.path.join(os.path.dirname(os.path.realpath(__file__)),'excels/tarjetero/rodelillo/Programa de Cardio Sector A 2019.xlsm')

    dataFrame = pd.read_excel(path, sheet_name='Datos')

    headers = dataFrame.columns

    counter = 0

    for i in range(0, len(dataFrame)):
        # Initialize variables

        # PSCV data

        lastControlDate = '1900-01-01'
        file = -1
        birthDate = '1900-01-01'
        admissionDate = '1900-01-01'
        sex = ''
        # pathologies
        hta = 0
        dm = 0
        dlp = 0
        hipo = 0
        epi = 0
        artrosis = 0
        #
        rcv = ''
        # IMC
        imc = -1.0
        # Examinations
        examinationDate = '1900-01-01'
        glic = -1.0
        col = -1.0
        ldl = -1.0
        hdl = -1.0
        tgc = -1.0
        crea = -1.0
        # Pressure
        pSistolica = -1.0
        pDiastolica = -1.0
        # Glycosylated hemoglobin
        hbg = -1.0
        hbgDate = '1900-01-01'

        # Rut
        temp = dataFrame[headers[1]][i]  # .replace(u'\xa0', u'')
        temp2 = dataFrame[headers[2]][i]
        try:
            temp = int(temp)
            docType = 'rut'
            doc = temp
            verifyingDigit = temp2
        except:
            docType = 'other'
            doc = None
            verifyingDigit = None

        if doc is not None:
            # Find patient using rut in the validated db
            query = {'documento.numero': str(doc)}

            result = collection.find_one(query)
            if result is not None:
                counter += 1

                # Date of last control

                excel_date = dataFrame[headers[67]][i]

                try:
                    if isinstance(excel_date, int):
                        dateNotUseful = datetime.date.fromordinal(
                            datetime.date(1900, 1, 1).toordinal() + excel_date - 2)
                        lastControlDate = dateNotUseful.strftime('%Y-%m-%d')
                    if isinstance(excel_date, datetime.date):
                        lastControlDate = excel_date.strftime('%Y-%m-%d')

                except TypeError:
                    print('Error en el sujeto: ' + dataFrame[headers[6]][i] +
                          '. El formato de fecha del último control es diferente al del resto del documento')
                    print('Tipo de dato: ' + str(type(excel_date)))

                # birthDate

                excel_birth_date = dataFrame[headers[4]][i]
                try:
                    if isinstance(excel_birth_date, int):
                        birthDateNotUseful = datetime.date.fromordinal(
                            datetime.date(1900, 1, 1).toordinal() + excel_birth_date - 2)
                        birthDate = birthDateNotUseful.strftime('%Y-%m-%d')
                    if isinstance(excel_birth_date, datetime.date) and not pd.isnull(excel_birth_date):
                        birthDate = excel_birth_date.strftime('%Y-%m-%d')

                except TypeError as e:
                    print(e)
                    print('Error en el sujeto: ' + dataFrame[headers[4]][i] +
                          '. El formato de fecha de nacimiento es diferente al del resto del documento')
                    print('Tipo de dato: ' + str(type(excel_birth_date)))

                # admissionDate

                excel_admission_date = dataFrame[headers[10]][i]

                if pd.isnull(excel_admission_date):
                    try:
                        if isinstance(excel_admission_date, int):
                            admissionDateNotUseful = datetime.date.fromordinal(
                                datetime.date(1900, 1, 1).toordinal() + excel_admission_date - 2)
                            admissionDate = admissionDateNotUseful.strftime('%Y-%m-%d')
                        if isinstance(excel_admission_date, datetime.date) and not 'NaT':
                            admissionDate = excel_admission_date.strftime('%Y-%m-%d')
                    except TypeError:
                        print('Error en el sujeto: ' + dataFrame[headers[10]][i] +
                              '. El formato de fecha es diferente al del resto del documento')
                else:
                    if isinstance(excel_admission_date, int):
                        excelAdmissionDateNotUseful = datetime.date.fromordinal(
                            datetime.date(1900, 1, 1).toordinal() + excel_admission_date - 2)
                        admissionDate = excelAdmissionDateNotUseful.strftime('%Y-%m-%d')

                    if isinstance(excel_admission_date, datetime.date) and not pd.isnull(excel_admission_date):
                        admissionDate = excel_admission_date.strftime('%Y-%m-%d')

                # Sex
                temp = dataFrame[headers[11]][i]
                if isinstance(temp, str) and temp == 'Masculino':
                    sex = 'M'
                if isinstance(temp, str) and temp == 'Femenino':
                    sex = 'F'

                # HTA & DM

                temp = dataFrame[headers[13]][i]
                if isinstance(temp, str) and temp == 'HTA':
                    hta = 1
                if isinstance(temp, str) and temp == 'DM':
                    dm = 1
                if isinstance(temp, str) and temp == 'MIXTA':
                    hta = 1
                    dm = 1

                # DLP
                temp = dataFrame[headers[31]][i]
                if isinstance(temp, str):
                    if 'HIPOTIROIDISMO' in temp or 'Hipo' in temp:
                        hipo = 1
                    if 'DISLIPIDEMIA' in temp or 'DISLIP' in temp or 'DISLIPIDEMIAS' in temp or 'Dislip' in temp:
                        dlp = 1
                    if 'ARTROSIS' in temp or 'Artrosis' in temp:
                        artrosis = 1
                    if 'EPILEPSIA' in temp or 'Epi' in temp:
                        epi = 1

                # RCV
                temp = dataFrame[headers[14]][i]

                if isinstance(temp, str) and temp == 'Bajo':
                    rcv = 'BAJO'
                if isinstance(temp, str) and temp == 'Moderado':
                    rcv = 'MODERADO'
                if isinstance(temp, str) and temp == 'Alto':
                    rcv = 'ALTO'

                # IMC

                # temp = dataFrame[headers[15]][i]
                # if isinstance(temp, str):
                #     imc = temp

                temp = dataFrame[headers[15]][i]
                if isinstance(temp, float) and not math.isnan(temp):
                    imc = np.round(temp, decimals=2)

                # Glicemia
                temp = dataFrame[headers[17]][i]
                if isinstance(temp, str):
                    glic = -1.0

                if isinstance(temp, int):
                    glic = float(temp)

                if isinstance(temp, float) and not math.isnan(temp):
                    glic = temp

                # Cholesterol

                temp = dataFrame[headers[23]][i]

                if isinstance(temp, str):
                    col = -1.0

                if isinstance(temp, int):
                    col = float(temp)

                if isinstance(temp, float) and not math.isnan(temp):
                    col = temp

                # print(glic, col)
                # LDL

                temp = dataFrame[headers[24]][i]

                if isinstance(temp, str):
                    ldl = -1.0

                if isinstance(temp, int):
                    ldl = float(temp)

                if isinstance(temp, float) and not math.isnan(temp):
                    ldl = temp

                # HDL
                temp = dataFrame[headers[25]][i]

                if isinstance(temp, str):
                    hdl = -1.0

                if isinstance(temp, int):
                    hdl = float(temp)

                if isinstance(temp, float) and not math.isnan(temp):
                    hdl = temp

                # print(ldl,hdl)

                # TGC

                temp = dataFrame[headers[26]][i]

                if isinstance(temp, str):
                    tgc = -1.0

                if isinstance(temp, int):
                    tgc = float(temp)

                if isinstance(temp, float) and not math.isnan(temp):
                    tgc = temp

                # Creatinina

                temp = dataFrame[headers[39]][i]

                if isinstance(temp, str):
                    crea = -1.0

                if isinstance(temp, int):
                    crea = float(temp)

                if isinstance(temp, float) and not math.isnan(temp):
                    crea = temp

                # print(tgc, crea)

                # Presión Sistolica

                temp = dataFrame[headers[27]][i]

                if isinstance(temp, float) and not math.isnan(temp):
                    pSistolica = np.round(temp, decimals=2)

                # Presión Diastolica

                temp = dataFrame[headers[28]][i]

                if isinstance(temp, float) and not math.isnan(temp):
                    pDiastolica = temp

                # print(pSistolica,pDiastolica)

                # Hemoglobina glicosilada

                temp = dataFrame[headers[30]][i]

                if isinstance(temp, float) and not math.isnan(temp):
                    hbg = temp
                if isinstance(temp, int) and not math.isnan(temp):
                    hbg = temp

                # hbgDate

                excel_hbg_date = dataFrame[headers[29]][i]
                if pd.isnull(excel_hbg_date):
                    try:
                        if isinstance(excel_hbg_date, int):
                            admissionDateNotUseful = datetime.date.fromordinal(
                                datetime.date(1900, 1, 1).toordinal() + excel_hbg_date - 2)
                            hbgDate = admissionDateNotUseful.strftime('%Y-%m-%d')
                        if isinstance(excel_hbg_date, datetime.date) and not 'NaT':
                            hbgDate = excel_hbg_date.strftime('%Y-%m-%d')
                    except TypeError:
                        print('Error en el sujeto: ' + dataFrame[headers[10]][i] +
                              '. El formato de fecha es diferente al del resto del documento')
                else:
                    try:
                        if isinstance(excel_hbg_date, int):
                            hbgDateNotUseful = datetime.date.fromordinal(
                                datetime.date(1900, 1, 1).toordinal() + excel_hbg_date - 2)
                            hbgDate = hbgDateNotUseful.strftime('%Y-%m-%d')
                        if isinstance(excel_hbg_date, datetime.date):
                            hbgDate = excel_hbg_date.strftime('%Y-%m-%d')

                    except TypeError:
                        print('Error en el sujeto: ' + dataFrame[headers[3]][i] +
                              '. El formato de fecha es diferente al del resto del documento')

                # print(hbg, hbgDate)

                # File

                temp = dataFrame[headers[3]][i]

                if isinstance(temp, int):
                    file = int(temp)

                # print(result)

                # print('file', type(file), 'should be: int')
                # print('lastControlDate', type(lastControlDate), 'should be: str')
                # print('admissionDate', type(admissionDate), 'should be: str')
                # print('hta', type(hta), 'should be: int')
                # print('dm', type(dm), 'should be: int')
                # print('disl', type(dlp), 'should be: int')
                # print('hipo', type(hipo), 'should be: int')
                # print('epi', type(epi), 'should be: int')
                # print('artrosis', type(artrosis), 'should be: int')
                # print('rcv', type(rcv), 'should be: str')
                # print('imc', type(imc), 'should be: float')
                # print('examinationDate', type(examinationDate), 'should be: str')
                # print('glic', type(glic), 'should be: float')
                # print('col', type(col), 'should be: float')
                # print('ldl', type(ldl), 'should be: float')
                # print('hdl', type(hdl), 'should be: float')
                # print('tgc', type(tgc), 'should be: float')
                # print('crea', type(crea), 'should be: float')
                # print('pSistolica', type(pSistolica), 'should be: float')
                # print('pDiastolica', type(pDiastolica), 'should be: float')
                # print('hbg', type(hbg), 'should be: float')
                # print('hbgDate', type(hbgDate), 'should be: str')
                # print('-------------------')

                data = {
                    'index': i,
                    'datosPersonales': {
                        'nombres': result['datosPersonales']['nombres'],
                        'apellido1': result['datosPersonales']['apellido1'],
                        'apellido2': result['datosPersonales']['apellido2'],
                        'genero': result['datosPersonales']['genero'],
                        'fechaNacimiento': result['datosPersonales']['fechaNacimiento']

                    },
                    'documento': {
                        'tipo': result['documento']['tipo'],
                        'numero': result['documento']['numero'],
                        'digitoVerificador': result['documento']['digitoVerificador']
                    },
                    'direccion': {
                        'numero': result['direccion']['numero'],
                        'calle': result['direccion']['calle'],
                        'ciudad': result['direccion']['ciudad'],
                        'pais': result['direccion']['pais']
                    },
                    'sector': result['sector'],
                    'geometry': {
                        'type': 'Point',
                        'coordinates': [result['geometry']['coordinates'][0], result['geometry']['coordinates'][1]]
                    },
                    'telefonos': {
                        'telefono1': result['telefonos']['telefono1'],
                        'telefono2': result['telefonos']['telefono2'],
                    },
                    'pscv': {
                        'numeroFicha': file,
                        'fechaUltimoControl': lastControlDate,
                        'fechaIngreso': admissionDate,
                        # 'fechaNacimiento': birthDate,
                        # 'sexo': sex,
                        'patologias': {
                            'hipertensionArterial': hta,
                            'diabetesMellitus': dm,
                            'dislipidemia': dlp,
                            'hipotiroidismo': hipo,
                            'epilepsia': epi,
                            'artrosis': artrosis
                        },
                        'riesgoCardiovascular': rcv,
                        'estadoNutricional': {
                            'imc': imc
                        },
                        'examenes': {
                            'fechaExamenes': examinationDate,
                            'glicemia': glic,
                            'colesterol': col,
                            'ldl': ldl,
                            'hdl': hdl,
                            'trigliceridos': tgc,
                            'creatinina': crea,
                        },
                        'presion': {
                            'presionSistolica': pSistolica,
                            'presionDiastolica': pDiastolica,
                        },
                        'hemoglobinaGlicosilada': {
                            'Hba1c': hbg,
                            'fechaHemoglobinaGlicosilada': hbgDate
                        }

                    }
                }
                print(data)
                print(counter)

                #destinationCollection.insert_one(data)

    print('-----------------------')
    print('success')
