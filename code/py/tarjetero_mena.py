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

    db = client["individuals-valparaiso"]

    ##
    # Mena DB

    collection = db["validated-mena-bbox"]
    destinationCollection = db["new-pscv-mena"]

    path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                        'excels/tarjetero/mena/new_TARJETERO PSCV Mena 2019.xlsx')

    dataFrame = pd.read_excel(path, sheet_name='TarjeteroLimpio')

    headers = dataFrame.columns

    counter = 0

    for i in range(0, len(dataFrame)):
        # for i in range(0, 20):

        # Initialize variables
        # PSCV data
        sex = None
        file = None

        lastControlDate = '1900-01-01'
        birthDate = '1900-01-01'
        admissionDate = '1900-01-01'
        examinationDate = '1900-01-01'
        hbgDate = '1900-01-01'
        racDate = '1900-01-01'
        ekgDate = '1900-01-01'
        nextControlDate = '1900-01-01'
        empamDate = '1900-01-01'
        podoDate = '1900-01-01'
        pieDate = '1900-01-01'
        colDate = '1900-01-01'
        creaDate = '1900-01-01'

        # pathologies
        hta = 0
        dm = 0
        dlp = 0
        hipo = 0
        epi = 0
        micro = -1.0
        artrosis = 0
        parkinson = 0
        tabaco = 0
        insulina = 0
        int_glu = 0

        # EMPAM
        vigencia = None

        # RCV
        rcv = None

        # IMC
        imc = -1.0
        peso = -1.0

        # Examinations
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

        # RAC
        rac = -1.0

        # EKG
        ekg = 0

        migrant = 0
        pOriginarios = 0
        retinoDiabet = 0
        hipo_or = 0
        ecvs = 0
        infarto = 0
        aspirina = 0
        estatinas = 0
        ieca = 0
        sospecha = 0
        act_fisica = 0
        insulino_ter = 0
        testUni = 0
        glicAyuno = 0
        vfg = -1.0
        statusControl = None
        comment = None
        statusNutrional = None
        func_diag = None
        podo = None
        statusRac = None
        statusPie = None
        pie = None
        statusCol = None
        statusCrea = None

        # Rut
        temp = dataFrame[headers[3]][i]  # .replace(u'\xa0', u'')
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
        # print('doc: ' + str(doc))

        # Find patient using rut in the validated db
        query = {'documento.numero': doc}
        result = collection.find_one({'documento.numero': doc})

        if result is not None:
            counter += 1

            # Date of last control
            excel_date = dataFrame[headers[11]][i]

            try:

                if isinstance(excel_date, int):
                    dateNotUseful = datetime.date.fromordinal(datetime.date(1900, 1, 1).toordinal() + excel_date - 2)
                    lastControlDate = dateNotUseful.strftime('%Y-%m-%d')
                if isinstance(excel_date, datetime.date):
                    lastControlDate = excel_date.strftime('%Y-%m-%d')

            except TypeError:
                print('Error en el sujeto: ' + dataFrame[headers[3]][i] +
                      '. El formato de fecha del último control es diferente al del resto del documento')
                print('Tipo de dato: ' + str(type(excel_date)))

            # birthDate
            excel_birth_date = dataFrame[headers[4]][i]
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

            # admissionDate
            excel_admission_date = dataFrame[headers[10]][i]
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

            # Sex
            temp = dataFrame[headers[9]][i]
            if isinstance(temp, float) and temp == 1:
                sex = 'MASCULINO'
            if isinstance(temp, float) and temp == 2:
                sex = 'FEMENINO'

            # Age
            temp = dataFrame[headers[5]][i]
            if pd.isnull(temp):
                age = -1.0
            elif isinstance(temp, float):
                age = int(temp)

            # HTA
            temp = dataFrame[headers[16]][i]
            if isinstance(temp, float) and temp == 1:
                hta = 1
            if isinstance(temp, float) and temp == 2:
                hta = 0

            # MICRO
            temp = dataFrame[headers[43]][i]
            if pd.isnull(temp):
                micro = -1.0
            elif isinstance(temp, float):
                micro = temp

            # DM
            temp = dataFrame[headers[16]][i]
            if isinstance(temp, float) and temp == 1:
                dm = 1
            if isinstance(temp, float) and temp == 2:
                dm = 0

            # PESO
            temp = dataFrame[headers[29]][i]
            if pd.isnull(temp):
                peso = 0
            elif isinstance(temp, float):
                peso = temp

            # PARKINSON
            temp = dataFrame[headers[22]][i]
            if isinstance(temp, float) and temp == 1:
                parkinson = 1
            if isinstance(temp, float) and temp == 2:
                parkinson = 0

            # INSULINA
            temp = dataFrame[headers[18]][i]
            if isinstance(temp, float) and temp == 1:
                insulina = 1
            if isinstance(temp, float) and temp == 2:
                insulina = 0

            # INTO GLU
            temp = dataFrame[headers[15]][i]
            if isinstance(temp, float) and temp == 1:
                int_glu = 1
            if isinstance(temp, float) and temp == 2:
                int_glu = 0

            # TABACO
            temp = dataFrame[headers[24]][i]
            if isinstance(temp, float) and temp == 1:
                parkinson = 1
            if isinstance(temp, float) and temp == 2:
                parkinson = 0

            # DLP
            temp = dataFrame[headers[19]][i]
            if isinstance(temp, float) and temp == 1:
                dlp = 1
            if isinstance(temp, float) and temp == 2:
                dlp = 0

            # HIPO
            temp = dataFrame[headers[20]][i]
            if isinstance(temp, float) and temp == 1:
                hipo = 1
            if isinstance(temp, float) and temp == 2:
                hipo = 0

            # EPI
            temp = dataFrame[headers[21]][i]
            if pd.isnull(temp):
                age = -1.0
            if isinstance(temp, float) and temp == 1:
                epi = 1
            if isinstance(temp, float) and temp == 2:
                epi = 0

            # ARTROSIS
            temp = dataFrame[headers[23]][i]
            if isinstance(temp, float) and temp == 1:
                artrosis = 1
            if isinstance(temp, float) and temp == 2:
                artrosis = 0

            # RCV
            temp = dataFrame[headers[27]][i]
            if pd.isnull(temp):
                rcv = None
            if isinstance(temp, float) and temp == 1:
                rcv = 'BAJO'
            if isinstance(temp, float) and temp == 2:
                rcv = 'MODERADO'
            if isinstance(temp, float) and temp == 3:
                rcv = 'ALTO'

            # RAC
            temp = dataFrame[headers[47]][i]
            if pd.isnull(temp):
                rac = -1.0
            elif isinstance(temp, float):
                rac = temp


            # RAC date
            temp = dataFrame[headers[46]][i]
            try:
                if isinstance(temp, int):
                    RacDateNotUseful = datetime.date.fromordinal(
                        datetime.date(1900, 1, 1).toordinal() + temp - 2)
                    racDate = RacDateNotUseful.strftime('%Y-%m-%d')
                if isinstance(temp, datetime.date):
                    racDate = temp.strftime('%Y-%m-%d')
            except:
                racDate = '1900-01-01'

            # IMC
            if pd.isnull(temp):
                imc = -1.0
            temp = dataFrame[headers[31]][i]
            if isinstance(temp, float) and not math.isnan(temp):
                imc = np.round(temp, decimals=2)

            # examinationDate
            excel_examination_date = dataFrame[headers[34]][i]
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

            # Glicemia
            temp = dataFrame[headers[39]][i]
            if isinstance(temp, str) or pd.isnull(temp):
                glic = -1.0
            if isinstance(temp, int):
                glic = float(temp)
            if isinstance(temp, float) and not math.isnan(temp):
                glic = temp

            # Cholesterol
            temp = dataFrame[headers[35]][i]
            if isinstance(temp, str) or pd.isnull(temp):
                col = -1.0
            if isinstance(temp, int):
                col = float(temp)
            if isinstance(temp, float) and not math.isnan(temp):
                col = temp

            # LDL
            temp = dataFrame[headers[37]][i]
            if isinstance(temp, str) or pd.isnull(temp):
                ldl = -1.0
            if isinstance(temp, int):
                ldl = float(temp)
            if isinstance(temp, float) and not math.isnan(temp):
                ldl = temp

            # HDL
            temp = dataFrame[headers[36]][i]
            if isinstance(temp, str) or pd.isnull(temp):
                hdl = -1.0
            if isinstance(temp, int):
                hdl = float(temp)
            if isinstance(temp, float) and not math.isnan(temp):
                hdl = temp

            # TGC
            temp = dataFrame[headers[38]][i]
            if isinstance(temp, str) or pd.isnull(temp):
                tgc = -1.0
            if isinstance(temp, int):
                tgc = float(temp)
            if isinstance(temp, float) and not math.isnan(temp):
                tgc = temp

            # Creatinina
            temp = dataFrame[headers[40]][i]
            if isinstance(temp, str) or pd.isnull(temp):
                crea = -1.0
            if isinstance(temp, int):
                crea = float(temp)
            if isinstance(temp, float) and not math.isnan(temp):
                crea = temp

            # Presión Sistolica
            temp = dataFrame[headers[32]][i]
            if pd.isnull(temp):
                pSistolica = -1.0
            if isinstance(temp, float) and not math.isnan(temp):
                pSistolica = np.round(temp, decimals=2)

            # Presión Diastolica
            temp = dataFrame[headers[33]][i]
            if pd.isnull(temp):
                pDiastolica = -1.0
            if isinstance(temp, float) and not math.isnan(temp):
                pDiastolica = temp

            # Hemoglobina glicosilada
            temp = dataFrame[headers[45]][i]
            if pd.isnull(temp):
                hbg = -1.0
            if isinstance(temp, float) and not math.isnan(temp):
                hbg = temp

            # vigencia
            temp = dataFrame[headers[60]][i]
            if pd.isnull(temp):
                vigencia = None
            if isinstance(temp, str):
                vigencia = temp

            # hbgDate
            excel_hbg_date = dataFrame[headers[44]][i]
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

            # EKGDate
            temp = dataFrame[headers[48]][i]
            try:
                if isinstance(temp, int):
                    ekgDateNotUseful = datetime.date.fromordinal(
                        datetime.date(1900, 1, 1).toordinal() + temp - 2)
                    ekgDate = ekgDateNotUseful.strftime('%Y-%m-%d')
                if isinstance(temp, datetime.date):
                    ekgDate = temp.strftime('%Y-%m-%d')
            except TypeError:
                print('Error en el sujeto: ' + dataFrame[headers[3]][i] +
                      '. El formato de fecha es diferente al del resto del documento')
            # VFG
            temp = dataFrame[headers[49]][i]
            if pd.isnull(temp):
                vfg = -1.0
            if isinstance(temp, float):
                vfg = temp

            # PieDiabetico
            temp = dataFrame[headers[55]][i]
            if pd.isnull(temp):
                pie = None
            if isinstance(temp, str):
                pie = temp

            # Fecha pieDiabetico
            temp = dataFrame[headers[54]][i]
            try:
                if isinstance(temp, int):
                    pieDateNotUseful = datetime.date.fromordinal(
                        datetime.date(1900, 1, 1).toordinal() + temp - 2)
                    pieDate = pieDateNotUseful.strftime('%Y-%m-%d')
                if isinstance(temp, datetime.date):
                    pieDate = temp.strftime('%Y-%m-%d')
            except:
                pieDate = '1990-01-01'

            # Podologia
            temp = dataFrame[headers[56]][i]
            try:
                if isinstance(temp, int):
                    podoDateNotUseful = datetime.date.fromordinal(
                        datetime.date(1900, 1, 1).toordinal() + temp - 2)
                    podoDate = podoDateNotUseful.strftime('%Y-%m-%d')
                if isinstance(temp, datetime.date):
                    podoDate = temp.strftime('%Y-%m-%d')
            except:
                podoDate = '1990-01-01'

            # Tratamiento
            # aspirina
            temp = dataFrame[headers[57]][i]
            if isinstance(temp, float):
                if temp == 1:
                    aspirina = 1
                elif temp == 2:
                    aspirina = 0

            # estatinas
            temp = dataFrame[headers[58]][i]
            if isinstance(temp, float):
                if temp == 1:
                    estatinas = 1
                elif temp == 2:
                    estatinas = 0

            temp = dataFrame[headers[0]][i]
            if isinstance(temp, int):
                file = temp

            # File
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
                    'cod': i,
                    'rut': result['documento']['numero'] + result['documento']['digitoVerificador'],
                    'nombreCompleto': result['datosPersonales']['nombres'] + ' ' + result['datosPersonales'][
                        'apellido1'] + ' ' + result['datosPersonales']['apellido2'],
                    'ficha': file,
                    'fechaNacimiento': birthDate,
                    'edad': age,
                    'sexo': sex,
                    'sector': result['sector'],
                    'fechaIngreso': admissionDate,
                    'migrante': migrant,
                    'pueblosOriginarios': pOriginarios,
                    'telefonos': {
                        'telefono1': result['telefonos']['telefono1'],
                        'telefono2': result['telefonos']['telefono2'],
                    },
                    'fechaUltimoControl': lastControlDate,
                    'fechaProximoControl': nextControlDate,
                    'estadoControl': statusControl,
                    'Comentario': comment,
                    'estadoNutricional': {
                        'imc': imc,
                        'peso': peso,
                        'estadoNutricional': statusNutrional
                    },
                    'riesgoCardiovascular': rcv,
                    'patologias': {
                        'diabetesMellitus': dm,
                        'hipertensionArterial': hta,
                        'epilepsia': epi,
                        'dislipidemia': dlp,
                        'tabaco': tabaco,
                        'artrosis': artrosis,
                        'parkinson': parkinson,
                        'hipotiroidismo': hipo,
                        'resistenciaInsulina': insulina,
                        'intoGlucosa': int_glu,
                        'retinopatiaDiabetica': retinoDiabet
                    },
                    'empam': {
                        'fechaEmpam': empamDate,
                        'estadoEfam': vigencia,
                        'diagnosticoFuncional': func_diag
                    },
                    'examenes': {
                        'fechaExamenes': examinationDate,
                        'ldl': ldl,
                        'hdl': hdl,
                        'glicemia': glic,
                        'trigliceridos': tgc,
                        'microalbuminuria': micro,
                        'podologo': podo,
                        'fechaPodologo': podoDate,
                        'rac': {
                            'fechaRac': racDate,
                            'resultadoRac': rac,
                            'estadoRac': statusRac
                        },
                        'pieDiabetico': {
                            'fechaPieDiabetico': pieDate,
                            'estadoPieDiabetico': statusPie,
                            'resultado': pie
                        },
                        'presion': {
                            'presionSistolica': pSistolica,
                            'presionDiastolica': pDiastolica,
                        },
                        'hemoglobinaGlicosilada': {
                            'Hba1c': hbg,
                            'fechaHemoglobinaGlicosilada': hbgDate
                        },
                        'colesterol': {
                            'fechaColesterol': colDate,
                            'estadoColesterol': statusCol,
                            'colesterolTotal': col,
                        },
                        'creatinina':
                            {'resultadoCreatinina': crea,
                             'estadoCreatinina': statusCrea,
                             'fechaCreatinina': creaDate
                             },
                        'ekg': {
                            'estadoEkg': ekg,
                            'fechaEkg': ekgDate,
                        }
                    },
                    'HipoglicemiantesOrales': hipo_or,
                    'antecedentes':
                        {
                            'ecvs': ecvs,
                            'infarto': infarto
                        },
                    'tratamientos':
                        {
                            'aspirina': aspirina,
                            'estatinas': estatinas,
                            'IECA': ieca
                        },
                    'sospechaMaltrato': sospecha,
                    'actividadFisica': act_fisica,
                    'VFG': vfg,
                    'insulinoterapia': insulino_ter,
                    'testUnipodal': testUni,
                    'glicemiaAyunoAlterada': glicAyuno
                }
            }

            print(data)
            print(counter)

            destinationCollection.insert_one(data)
            print('-----------------------')
