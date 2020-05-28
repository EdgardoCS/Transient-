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
    # Cordillera DB

    collection = db['validated-cordillera-bbox']

    destinationCollection = db["pscv-cordillera"]

    #path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
    #                   'excels/tarjetero/cordillera/Cordillera Sector  1.xls')
    #dataFrame = pd.read_excel(path, sheet_name='CARDIOVASCULAR SECTOR 1 ')

    path = os.path.join(os.path.dirname(os.path.realpath(__file__)),'excels/tarjetero/cordillera/Cordillera Sector 2.xlsx')
    dataFrame = pd.read_excel(path, sheet_name='CV VIGENTES')

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
        temp = dataFrame[headers[3]][i]

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
            # Find patient using rut in the validated db
            query = {'documento.numero': doc}

            result = collection.find_one(query)
            if result is not None:
                counter += 1

                # Date of last control

                excel_date = dataFrame[headers[2]][i]
                try:
                    if isinstance(excel_date, int):
                        dateNotUseful = datetime.date.fromordinal(
                            datetime.date(1900, 1, 1).toordinal() + excel_date - 2)
                        lastControlDate = dateNotUseful.strftime('%Y-%m-%d')
                    if isinstance(excel_date, datetime.date):
                        lastControlDate = excel_date.strftime('%Y-%m-%d')

                except TypeError:
                    print('Error en el sujeto: ' + dataFrame[headers[2]][i] +
                          '. El formato de fecha del último control es diferente al del resto del documento')
                    print('Tipo de dato: ' + str(type(excel_date)))

                # birthDate

                excel_birth_date = dataFrame[headers[7]][i]
                try:
                    if isinstance(excel_birth_date, int):
                        birthDateNotUseful = datetime.date.fromordinal(
                            datetime.date(1900, 1, 1).toordinal() + excel_birth_date - 2)
                        birthDate = birthDateNotUseful.strftime('%Y-%m-%d')
                    if isinstance(excel_birth_date, datetime.date) and not pd.isnull(excel_birth_date):
                        birthDate = excel_birth_date.strftime('%Y-%m-%d')

                except TypeError as e:
                    print(e)
                    print('Error en el sujeto: ' + dataFrame[headers[7]][i] +
                          '. El formato de fecha de nacimiento es diferente al del resto del documento')
                    print('Tipo de dato: ' + str(type(excel_birth_date)))

                # admissionDate

                excel_admission_date = dataFrame[headers[1]][i]

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
                # print(lastControlDate, birthDate, admissionDate)

                # Sex
                temp = dataFrame[headers[9]][i]
                if isinstance(temp, str) and temp == 'MASCULINO':
                    sex = 'M'
                if isinstance(temp, str) and temp == 'FEMENINO':
                    sex = 'F'
                # print(sex)

                # HTA / DM / ARTROSIS / DISLIPIDEMIA / EPI / HIPO
                temp = dataFrame[headers[10]][i]
                if isinstance(temp, str) and temp == 'HTA':
                    hta = 1
                if isinstance(temp, str) and temp == 'DM':
                    dm = 1
                if isinstance(temp, str) and temp == 'MIXTO':
                    hta = 1
                    dm = 1
                if isinstance(temp, str) and temp == 'ARTROSIS':
                    artrosis = 1
                if isinstance(temp, str) and temp == 'DISLIPIDEMIA':
                    dlp = 1
                if isinstance(temp, str) and temp == 'EPI':
                    epi = 1
                if isinstance(temp, str) and temp == 'HIPO':
                    hipo = 1

                # print(hta, dm, artrosis,dlp ,hipo,epi)

                # RCV
                temp = dataFrame[headers[11]][i]

                if isinstance(temp, str) and temp == 'LEVE':
                    rcv = 'BAJO'
                if isinstance(temp, str) and temp == 'MODERADO':
                    rcv = 'MODERADO'
                if isinstance(temp, str) and temp == 'ALTO':
                    rcv = 'ALTO'
                # print(rcv)

                '''
                # IMC
                temp = dataFrame[headers[15]][i]
                if isinstance(temp, float) and not math.isnan(temp):
                    imc = np.round(temp, decimals=2)

                # Glicemia  glicemia is not presented
                # temp = dataFrame[headers[17]][i]
                # if isinstance(temp, str):
                #     glic = -1.0
                #
                # if isinstance(temp, int):
                #     glic = float(temp)
                #
                # if isinstance(temp, float) and not math.isnan(temp):
                #     glic = temp

                # Cholesterol

                temp = dataFrame[headers[35]][i]
                if isinstance(temp, str):
                    col = -1.0

                if isinstance(temp, int):
                    col = float(temp)

                if isinstance(temp, float) and not math.isnan(temp):
                    col = temp

                #print(glic, col)
                # LDL

                temp = dataFrame[headers[38]][i]

                if isinstance(temp, str):
                    ldl = -1.0

                if isinstance(temp, int):
                    ldl = float(temp)

                if isinstance(temp, float) and not math.isnan(temp):
                    ldl = temp

                # HDL
                temp = dataFrame[headers[37]][i]

                if isinstance(temp, str):
                    hdl = -1.0

                if isinstance(temp, int):
                    hdl = float(temp)

                if isinstance(temp, float) and not math.isnan(temp):
                    hdl = temp

                # print(ldl,hdl)

                # TGC

                temp = dataFrame[headers[36]][i]

                if isinstance(temp, str):
                    tgc = -1.0

                if isinstance(temp, int):
                    tgc = float(temp)

                if isinstance(temp, float) and not math.isnan(temp):
                    tgc = temp

                # Creatinina

                temp = dataFrame[headers[34]][i]

                if isinstance(temp, str):
                    crea = -1.0

                if isinstance(temp, int):
                    crea = float(temp)

                if isinstance(temp, float) and not math.isnan(temp):
                    crea = temp
                    
                # print(tgc, crea)
                '''
                # IMC
                # temp = dataFrame[headers[15]][i]
                # if isinstance(temp, str):
                #    imc = temp.lower()

                # Glicemia  glicemia is not presented

                # Cholesterol
                temp = dataFrame[headers[35]][i]
                if isinstance(temp, str):
                    if '<' in temp:
                        _temp = temp.split('<')
                        __temp = _temp[1].split(')')
                        col = float(__temp[0])
                    if '>' in temp:
                        _temp = temp.split('>')
                        __temp = _temp[1].split(')')
                        col = float(__temp[0])

                # LDL
                temp = dataFrame[headers[38]][i]
                if isinstance(temp, str):
                    if '<' in temp:
                        _temp = temp.split('<')
                        __temp = _temp[1].split(')')
                        ldl = float(__temp[0])
                    if '>' in temp:
                        _temp = temp.split('>')
                        __temp = _temp[1].split(')')
                        ldl = float(__temp[0])

                # HDL
                temp = dataFrame[headers[37]][i]
                if isinstance(temp, str):
                    if '<' in temp:
                        _temp = temp.split('<')
                        __temp = _temp[1].split(')')
                        hdl = float(__temp[0])
                    if '>' in temp:
                        _temp = temp.split('>')
                        __temp = _temp[1].split(')')
                        hdl = float(__temp[0])

                # print(imc, col,ldl,hdl)

                # TGC
                temp = dataFrame[headers[36]][i]
                if isinstance(temp, str):
                    if '<' in temp:
                        _temp = temp.split('<')
                        __temp = _temp[1].split(')')
                        tgc = float(__temp[0])
                    if '>' in temp:
                        _temp = temp.split('>')
                        __temp = _temp[1].split(')')
                        tgc = float(__temp[0])

                # Creatinina
                temp = dataFrame[headers[34]][i]

                if isinstance(temp, str):
                    if len(temp) >= 9:
                        _temp = temp.strip('(').strip(')').replace(',', '.')
                        __temp = _temp.split('-')
                        crea = round((float(__temp[1]) + float(__temp[0])) / 2, 3)
                        # print(crea)
                    else:
                        if '<' in temp:
                            _temp = temp.split('<')
                            __temp = _temp[1].split(')')
                            crea = float(__temp[0].replace(',', '.'))
                        if '>' in temp:
                            _temp = temp.split('>')
                            __temp = _temp[1].split(')')
                            crea = float(__temp[0].replace(',', '.'))

                # print(tgc, crea)
                # PSistolica / PDiastolica
                temp = dataFrame[headers[16]][i]
                if isinstance(temp, str):
                    if '(<)' in temp or '(>)' in temp:
                        temp = temp.split(')')[1]
                    if '(+)' in temp or '(-)' in temp:
                        temp = temp.split(')')[1]
                    _temp = temp.split('/')
                    pSistolica = float(np.round(int(_temp[0]), decimals=2))
                    pDiastolica = float(np.round(int(_temp[1]), decimals=2))
                # print(pSistolica, pDiastolica)

                # Hemoglobina glicosilada
                temp = dataFrame[headers[32]][i]
                if isinstance(temp, float) and not math.isnan(temp):
                    hbg = float(temp)
                if isinstance(temp, int) and not math.isnan(temp):
                    hbg = float(temp)

                # hbgDate
                excel_hbg_date = dataFrame[headers[31]][i]
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

                temp = dataFrame[headers[0]][i]

                if isinstance(temp, int):
                    file = int(temp)

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
