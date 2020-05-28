import pymongo
import pandas as pd
import datetime
import numpy as np
import math

import os

import time

if __name__ == '__main__':

    ##
    # Note: this script only works with pymongo 3.8
    client = pymongo.MongoClient("mongodb://localhost:27017/")

    db = client['individuals-valparaiso']

    ##
    # Baron DB

    collection = db['validated-baron-bbox']
    # collection = db["validated-padre-damian-bbox"]

    destinationCollection = db["pscv-baron"]

    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'excels/tarjetero/baron/TARJETERO CARDIO OCTUBRE 2018 Barón.xlsx')

    dataFrame = pd.read_excel(path, sheet_name='2018')

    headers = dataFrame.columns

    counter = 0

    for i in range(0, len(dataFrame)):
    #for i in range(0,20):
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

        temp = dataFrame[headers[6]][i]  # .replace(u'\xa0', u'')
        # print(temp)

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

                excel_date = dataFrame[headers[49]][i]

                try:
                    if isinstance(excel_date, int):
                        dateNotUseful = datetime.date.fromordinal(datetime.date(1900, 1, 1).toordinal() + excel_date - 2)
                        lastControlDate = dateNotUseful.strftime('%Y-%m-%d')
                    if isinstance(excel_date, datetime.date):
                        lastControlDate = excel_date.strftime('%Y-%m-%d')

                except TypeError:
                    print('Error en el sujeto: ' + dataFrame[headers[6]][i] +
                          '. El formato de fecha del último control es diferente al del resto del documento')
                    print('Tipo de dato: ' + str(type(excel_date)))

                # print('lastControlDate')
                # print(lastControlDate)

                # birthDate

                excel_birth_date = dataFrame[headers[8]][i]
                try:
                    if isinstance(excel_birth_date, int):
                        birthDateNotUseful = datetime.date.fromordinal(
                            datetime.date(1900, 1, 1).toordinal() + excel_birth_date - 2)
                        birthDate = birthDateNotUseful.strftime('%Y-%m-%d')
                    if isinstance(excel_birth_date, datetime.date) and not pd.isnull(excel_birth_date):
                        birthDate = excel_birth_date.strftime('%Y-%m-%d')

                except TypeError as e:
                    print(e)
                    print('Error en el sujeto: ' + dataFrame[headers[6]][i] +
                          '. El formato de fecha de nacimiento es diferente al del resto del documento')
                    print('Tipo de dato: ' + str(type(excel_birth_date)))

                # print('birthDate')
                # print(birthDate)

                # admissionDate

                excel_admission_date = dataFrame[headers[10]][i]
                excel_admission_date2 = dataFrame[headers[11]][i]

                if pd.isnull(excel_admission_date):
                    try:
                        if isinstance(excel_admission_date2, int):
                            admissionDateNotUseful = datetime.date.fromordinal(
                                datetime.date(1900, 1, 1).toordinal() + excel_admission_date2 - 2)
                            admissionDate = admissionDateNotUseful.strftime('%Y-%m-%d')
                        if isinstance(excel_admission_date2, datetime.date):
                            admissionDate = excel_admission_date2.strftime('%Y-%m-%d')
                    except TypeError:
                        print('Error en el sujeto: ' + dataFrame[headers[6]][i] +
                              '. El formato de fecha es diferente al del resto del documento')
                else:
                    try:
                        if isinstance(excel_admission_date, int):
                            admissionDateNotUseful = datetime.date.fromordinal(
                                datetime.date(1900, 1, 1).toordinal() + excel_admission_date - 2)
                            admissionDate = admissionDateNotUseful.strftime('%Y-%m-%d')
                        if isinstance(excel_admission_date, datetime.date):
                            admissionDate = excel_admission_date.strftime('%Y-%m-%d')

                    except TypeError:
                        print('Error en el sujeto: ' + dataFrame[headers[6]][i] +
                              '. El formato de fecha es diferente al del resto del documento')

                # print('admissionDate')
                # print(admissionDate)

                # Sex
                temp = dataFrame[headers[12]][i]
                if isinstance(temp, str) and temp == 'Masculino':
                    sex = 'M'
                if isinstance(temp, str) and temp == 'Femenino':
                    sex = 'F'

                # print('sex')
                # print(sex)

                # HTA & DM

                temp = dataFrame[headers[14]][i]

                if isinstance(temp, str) and temp == 'HTA':
                    hta = 1
                if isinstance(temp, str) and temp == 'DM':
                    dm = 1
                if isinstance(temp, str) and temp == 'MIXTA':
                    hta = 1
                    dm = 1

                # print('hta,dm')
                # print(hta,',',dm)

                # DLP

                temp = dataFrame[headers[37]][i]

                if isinstance(temp, float) and temp == 1:
                    dlp = 1

                # print('dlp')
                # print(dlp)

                # HIPO
                # Hipotiroidismo está dentro de patologias, no se sabe si mixta hace referencia
                # solo a DM + HTA o incluye HIPOT
                temp = dataFrame[headers[14]][i]

                if isinstance(temp, str) and temp == 'HIPOT':
                    hipo = 1

                # print('hipo')
                # print(hipo)

                # EPI - ARTROSIS

                temp = dataFrame[headers[52]][i]

                if isinstance(temp, str) and temp == 'EPI':
                    epi = 1
                if isinstance(temp, str) and temp == 'ARTROSIS':
                    artrosis = 1
                # print('epi')
                # print(epi)
                # print('artrosis')
                # print(artrosis)

                # RCV

                temp = dataFrame[headers[24]][i]

                if isinstance(temp, str) and temp == 'Bajo':
                    rcv = 'BAJO'
                if isinstance(temp, str) and temp == 'Moderado':
                    rcv = 'MODERADO'
                if isinstance(temp, str) and temp == 'Alto':
                    rcv = 'ALTO'

                #print('rcv')
                #print(rcv)


                # IMC

                temp = dataFrame[headers[28]][i]

                if isinstance(temp, float) and not math.isnan(temp):
                    imc = np.round(temp, decimals=2)

                #print('imc')
                #print(imc)

                # examinationDate

                # excel_examination_date = dataFrame[headers[43]][i]
                #
                # try:
                #
                #     if isinstance(excel_examination_date, int):
                #         examinationDateNotUseful = datetime.date.fromordinal(
                #             datetime.date(1900, 1, 1).toordinal() + excel_examination_date - 2)
                #         examinationDate = examinationDateNotUseful.strftime('%Y-%m-%d')
                #     if isinstance(excel_examination_date, datetime.date):
                #         examinationDate = excel_examination_date.strftime('%Y-%m-%d')
                #
                # except TypeError:
                #     print('Error en el sujeto: ' + dataFrame[headers[3]][i] +
                #           '. El formato de fecha es diferente al del resto del documento')

                #print('examinationDate')
                #print(examinationDate)


                # Glicemia

                temp = dataFrame[headers[35]][i]

                if isinstance(temp, str):
                    glic = -1.0

                if isinstance(temp, int):
                    glic = float(temp)

                if isinstance(temp, float) and not math.isnan(temp):
                    glic = temp

                #print('glic')
                #print(glic)


                # Cholesterol

                temp = dataFrame[headers[38]][i]

                if isinstance(temp, str):
                    col = -1.0

                if isinstance(temp, int):
                    col = float(temp)

                if isinstance(temp, float) and not math.isnan(temp):
                    col = temp

                #print('col')
                #print(col)

                # LDL

                temp = dataFrame[headers[41]][i]

                if isinstance(temp, str):
                    ldl = -1.0

                if isinstance(temp, int):
                    ldl = float(temp)

                if isinstance(temp, float) and not math.isnan(temp):
                    ldl = temp

                #print('ldl')
                #print(ldl)


                # HDL

                temp = dataFrame[headers[40]][i]

                if isinstance(temp, str):
                    hdl = -1.0

                if isinstance(temp, int):
                    hdl = float(temp)

                if isinstance(temp, float) and not math.isnan(temp):
                    hdl = temp

                #print('hdl')
                #print(hdl)


                # TGC

                temp = dataFrame[headers[39]][i]

                if isinstance(temp, str):
                    tgc = -1.0

                if isinstance(temp, int):
                    tgc = float(temp)

                if isinstance(temp, float) and not math.isnan(temp):
                    tgc = temp

                #print('tgc')
                #print(tgc)


                # Creatinina

                temp = dataFrame[headers[36]][i]

                if isinstance(temp, str):
                    crea = -1.0

                if isinstance(temp, int):
                    crea = float(temp)

                if isinstance(temp, float) and not math.isnan(temp):
                    crea = temp

                #print('crea')
                #print(crea)

                # Presión Sistolica

                temp = dataFrame[headers[31]][i]

                if isinstance(temp, float) and not math.isnan(temp):
                    pSistolica = np.round(temp, decimals=2)

                #print('pSistolica')
                #print(pSistolica)

                # Presión Diastolica

                temp = dataFrame[headers[32]][i]

                if isinstance(temp, float) and not math.isnan(temp):
                   pDiastolica = temp

                #print('pDiastolica')
                #print(pDiastolica)

                # Hemoglobina glicosilada

                temp = dataFrame[headers[42]][i]

                if isinstance(temp, float) and not math.isnan(temp):
                    hbg = temp
                if isinstance(temp, int) and not math.isnan(temp):
                    hbg = temp

                #print('hbg')
                #print(hbg)

                # hbgDate

                excel_hbg_date = dataFrame[headers[43]][i]

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

                #print('hbgDate')
                #print(hbgDate)

                # File

                temp = dataFrame[headers[0]][i]

                if isinstance(temp, np.int64):
                    file = int(temp)

                #print('file')
                #print(file)

                #print(result)

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
                print(counter)
                print(data)

                #destinationCollection.insert_one(data)
    print('-----------------------')
    print('success')
