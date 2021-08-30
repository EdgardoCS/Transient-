import pandas as pd
import numpy as np
import pymongo
import datetime
import math

import os
import time

if __name__ == '__main__':

    # Note: this script only works with pymongo 3.8

    client = pymongo.MongoClient("mongodb://localhost:27017/")

    db = client['individuals-valparaiso']

    ##
    # PadreDamian DB

    collection = db['validated-padre-damian-bbox']

    destinationCollection = db["pscv-padre-damian"]

    # path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
    #                   'excels/tarjetero/padre damian/Padre Damián SECTOR 1.xlsx')
    # dataFrame = pd.read_excel(path, sheet_name='CRONICOS')

    path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                        'excels/tarjetero/padre damian/Padre Damián SECTOR 2.xlsx')
    dataFrame = pd.read_excel(path, sheet_name='Hoja1')

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

        if isinstance(temp, str):
            tempRut = temp.split('-')

            if len(tempRut) > 1:
                docType = 'rut'
                doc = tempRut[0].strip()
                verifyingDigit = tempRut[1].strip()
            else:
                docType = 'other'
                doc = temp
                verifyingDigit = temp

        else:
            docType = 'other'
            doc = None
            verifyingDigit = None

        if doc is not None:
            # print('doc: ' + str(doc))
            # Find patient using rut in the validated db

            query = {'documento.numero': doc}
            # print(collection.count_documents({'documento.numero': doc}))

            result = collection.find_one(query)

            if result is not None:
                counter += 1

                # Date of last control

                excel_date = dataFrame[headers[56]][i]

                try:
                    if isinstance(excel_date, int):
                        dateNotUseful = datetime.date.fromordinal(
                            datetime.date(1900, 1, 1).toordinal() + excel_date - 2)
                        lastControlDate = dateNotUseful.strftime('%Y-%m-%d')
                    if isinstance(excel_date, datetime.date):
                        lastControlDate = excel_date.strftime('%Y-%m-%d')

                except TypeError:
                    print('Error en el sujeto: ' + dataFrame[headers[3]][i] +
                          '. El formato de fecha del último control es diferente al del resto del documento')
                    print('Tipo de dato: ' + str(type(excel_date)))

                # print('lastControlDate')
                # print(lastControlDate)

                # birthDate

                excel_birth_date = dataFrame[headers[3]][i]

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

                # print('birthDate')
                # print(type(birthDate), birthDate)

                # admissionDate

                excel_admission_date = dataFrame[headers[9]][i]

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

                # print('admissionDate')
                # print(admissionDate)

                # Sex

                temp = dataFrame[headers[10]][i]

                if isinstance(temp, str) and temp == 'Masculino':
                    sex = 'M'
                if isinstance(temp, str) and temp == 'Femenino':
                    sex = 'F'

                # print('sex')
                # print(sex)

                # HTA | DM

                temp = dataFrame[headers[11]][i]

                if isinstance(temp, str) and temp == 'HTA':
                    hta = 1
                if isinstance(temp, str) and temp == 'DM':
                    dm = 1
                if isinstance(temp, str) and temp == 'MIXTA':
                    hta = 1
                    dm = 1
                if isinstance(temp, str) and temp == 'MIXTO':
                    hta = 1
                    dm = 1
                # print('hta')
                # print(hta)
                # print('dm')
                # print(dm)

                # DLP

                temp = dataFrame[headers[12]][i]

                if isinstance(temp, str):
                    if 'hipo' in temp or 'Hipo' in temp:
                        hipo = 1
                    if 'disl' in temp or 'Disl' in temp or 'dlp' in temp or 'DLP' in temp:
                        dlp = 1
                    if 'artrosis' in temp or 'Artrosis' in temp:
                        artosis = 1
                    if 'epi' in temp or 'Epi' in temp:
                        epi = 1

                # RCV

                temp = dataFrame[headers[29]][i]

                if isinstance(temp, str) and temp == 'Bajo':
                    rcv = 'BAJO'
                if isinstance(temp, str) and temp == 'Medio':
                    rcv = 'MODERADO'
                if isinstance(temp, str) and temp == 'Alto':
                    rcv = 'ALTO'

                # print('rcv')
                # print(rcv)

                # IMC

                temp = dataFrame[headers[19]][i]
                if isinstance(temp, float) and not math.isnan(temp):
                    imc = np.round(temp, decimals=2)

                # print('imc')
                # print(imc)

                # examinationDate

                excel_examination_date = dataFrame[headers[36]][i]

                try:

                    if isinstance(excel_examination_date, int):
                        examinationDateNotUseful = datetime.date.fromordinal(
                            datetime.date(1900, 1, 1).toordinal() + excel_examination_date - 2)
                        examinationDate = examinationDateNotUseful.strftime('%Y-%m-%d')
                    if isinstance(excel_examination_date, datetime.date):
                        examinationDate = excel_examination_date.strftime('%Y-%m-%d')

                except TypeError:
                    print('Error en el sujeto: ' + dataFrame[headers[3]][i] +
                          '. El formato de fecha es diferente al del resto del documento')

                # print('examinationDate')
                # print(examinationDate)

                # Glicemia

                temp = dataFrame[headers[35]][i]

                if isinstance(temp, str):
                    glic = -1.0

                if isinstance(temp, int):
                    glic = float(temp)

                if isinstance(temp, float) and not math.isnan(temp):
                    glic = temp

                # print('glic')
                # print(glic)

                # Cholesterol

                temp = dataFrame[headers[37]][i]

                if isinstance(temp, str):
                    col = -1.0

                if isinstance(temp, int):
                    col = float(temp)

                if isinstance(temp, float) and not math.isnan(temp):
                    col = temp

                # print('col')
                # print(col)

                # LDL

                temp = dataFrame[headers[38]][i]

                if isinstance(temp, str):
                    ldl = -1.0

                if isinstance(temp, int):
                    ldl = float(temp)

                if isinstance(temp, float) and not math.isnan(temp):
                    ldl = temp

                # print('ldl')
                # print(ldl)

                # HDL

                temp = dataFrame[headers[40]][i]

                if isinstance(temp, str):
                    hdl = -1.0

                if isinstance(temp, int):
                    hdl = float(temp)

                if isinstance(temp, float) and not math.isnan(temp):
                    hdl = temp

                # print('hdl')
                # print(hdl)

                # TGC

                temp = dataFrame[headers[41]][i]

                if isinstance(temp, str):
                    tgc = -1.0

                if isinstance(temp, int):
                    tgc = float(temp)

                if isinstance(temp, float) and not math.isnan(temp):
                    tgc = temp

                # print('tgc')
                # print(tgc)

                # Creatinina

                temp = dataFrame[headers[46]][i]

                if isinstance(temp, str):
                    crea = -1.0

                if isinstance(temp, int):
                    crea = float(temp)

                if isinstance(temp, float) and not math.isnan(temp):
                    crea = temp

                # print('crea')
                # print(crea)

                # Presión Sistolica

                temp = dataFrame[headers[20]][i]

                if isinstance(temp, float) and not math.isnan(temp):
                    pSistolica = np.round(temp, decimals=2)

                # print('pSistolica')
                # print(pSistolica)

                # Presión Diastolica

                temp = dataFrame[headers[22]][i]

                if isinstance(temp, float) and not math.isnan(temp):
                    pDiastolica = temp

                # print('pDiastolica')
                # print(pDiastolica)

                # Hemoglobina glicosilada

                temp = dataFrame[headers[42]][i]

                if isinstance(temp, float) and not math.isnan(temp):
                    hbg = temp

                # print('hbg')
                # print(hbg)

                # hbgDate  | hbhDate not presented

                # excel_hbg_date = dataFrame[headers[44]][i]
                # print('excel_hbg_date')
                # print(excel_hbg_date)
                # print(type(excel_hbg_date))
                #
                # try:
                #
                #     if isinstance(excel_hbg_date, int):
                #         hbgDateNotUseful = datetime.date.fromordinal(
                #             datetime.date(1900, 1, 1).toordinal() + excel_hbg_date - 2)
                #         hbgDate = hbgDateNotUseful.strftime('%Y-%m-%d')
                #     if isinstance(excel_hbg_date, datetime.date):
                #         hbgDate = excel_hbg_date.strftime('%Y-%m-%d')
                #
                # except TypeError:
                #     print('Error en el sujeto: ' + dataFrame[headers[3]][i] +
                #           '. El formato de fecha es diferente al del resto del documento')
                #
                # print('hbgDate')
                # print(hbgDate)

                # File

                temp = dataFrame[headers[2]][i]

                if isinstance(temp, float):
                    file = int(temp)

                # print('file')
                # print(file)

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
