import pymongo
import pandas as pd
import datetime
import numpy as np
import math
import os
from pathlib import Path
from dateutil.relativedelta import relativedelta

import time

if __name__ == '__main__':
    ##
    # Note: this script only works with pymongo 3.8

    client = pymongo.MongoClient("mongodb://localhost:27017/")

    db = client["individuals-valparaiso"]

    ##
    # Mena DB

    # collection = db["validated-mena-bbox"]

    destinationCollection = db["full-pscv-mena"]

    path = os.path.join(Path('/home/ed/Documents/Projects'),
                        'excels/tarjetero/mena/NUEVO TARJETERO CV 2019.xlsx')

    dataFrame = pd.read_excel(path, sheet_name='TARJETERO_CLEAN')

    headers = dataFrame.columns

    counter = 0

    for i in range(0, len(dataFrame)):

        # Initialize variables
        # PSCV data
        cod = 0
        doc = None

        name = None
        lastName1 = None
        lastName2 = None
        file = None
        birthDate = '1900-01-01'
        age = -1
        sex = None
        sector = None
        admissionDate = '1900-01-01'
        migrant = 0
        pOriginarios = 0
        phone = None

        lastControlDate = '1900-01-01'
        nextControlDate = '1900-01-01'
        controlStatus = None
        comment = None

        peso = -1.0
        imc = -1.0
        nutrionalStatus = None
        rcv = None

        dm = 0
        hta = 0
        epi = 0
        dlp = 0
        tabaco = 0
        artrosis = 0
        parkinson = 0
        hipo = 0
        insulina = 0
        int_glu = 0
        retinoDiabet = 0

        empamDate = '1900-01-01'
        efamStatus = None
        func_diag = None

        hbgDate = '1900-01-01'
        hbg = -1.0

        colDate = '1900-01-01'
        colStatus = None
        col = -1.0

        ldl = -1.0
        hdl = -1.0
        tgc = -1.0

        ekgDate = '1900-01-01'
        ekgStatus = None

        creaDate = '1900-01-01'
        creaStatus = None
        crea = -1.0

        micro = -1.0
        glic = -1.0

        racDate = '1900-01-01'
        racStatus = None
        rac = -1.0

        pieDate = '1900-01-01'
        pieStatus = None
        pie = None

        podo = None
        podoDate = '1900-01-01'

        pSistolica = -1.0
        pDiastolica = -1.0

        hipo_or = 0  # hipoglicemiantes orales

        ecvs = 0
        infarto = 0

        aspirina = 0
        estatinas = 0
        ieca = 0

        sospecha = 0
        act_fisica = 0

        vfg = -1.0
        insulino_ter = 0
        tug = 0  # timeupandgo
        testUni = 0
        glicAyuno = 0

        # CONTROL
        vigencia = None

        # File
        temp = dataFrame[headers[0]][i]
        if isinstance(temp, int):
            file = temp

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

        # Find patient using rut
        # query = {'documento.numero': doc}
        # result = collection.find_one(query)

        if doc is not None:

            # print('doc: ' + str(doc) + '-' + verifyingDigit)

            counter += 1

            # Name
            temp = dataFrame[headers[6]][i]
            if pd.isnull(temp):
                name = None
            elif isinstance(temp, str):
                name = temp

            # lastName
            temp = dataFrame[headers[7]][i]
            if pd.isnull(temp):
                lastName1 = None
            elif isinstance(temp, str):
                lastName1 = temp

            temp = dataFrame[headers[8]][i]
            if pd.isnull(temp):
                lastName2 = None
            elif isinstance(temp, str):
                lastName2 = temp
            try:
                fullName = name + ' ' + lastName1 + ' ' + lastName2
            except:
                fullName = None
            # print(fullName, type(fullName), 'should be str')

            # birthDate
            excel_birth_date = dataFrame[headers[4]][i]
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

            # Age
            temp = dataFrame[headers[5]][i]
            if pd.isnull(temp):
                age = -1
            elif isinstance(temp, np.int64):
                age = int(temp)
            # print(age, type(age), 'should be int')

            # Sex
            temp = dataFrame[headers[9]][i]
            if pd.isnull(temp):
                sex = None
            if isinstance(temp, np.int64) and temp == 1:
                sex = 'MASCULINO'
            if isinstance(temp, np.int64) and temp == 2:
                sex = 'FEMENINO'
            # print(sex, type(sex), 'should be str')

            # Sector
            temp = dataFrame[headers[1]][i]
            if pd.isnull(temp):
                sector = None
            elif isinstance(temp, np.int64):
                sector = int(temp)
            # print(sector, type(sector), 'should be int')

            # admissionDate
            excel_admission_date = dataFrame[headers[10]][i]
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

            # Migrant
            # unregistered

            # PuebloOriginario
            # unregistered

            # Phone
            # unregistered

            # lastControlDate
            excel_date = dataFrame[headers[11]][i]
            if pd.isnull(excel_date):
                lastControlDate = '1900-01-01'
            elif isinstance(excel_date, str):
                lastControlDate = '1900-01-01'
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
            # print(lastControlDate, type(lastControlDate), 'should be str')

            # nextControlDate
            temp = dataFrame[headers[13]][i]
            if pd.isnull(temp):
                nextControlDate = '1900-01-01'
            elif isinstance(temp, str):
                nextControlDate = '1900-01-01'
            try:
                if isinstance(temp, int):
                    dateNotUseful = datetime.date.fromordinal(
                        datetime.date(1900, 1, 1).toordinal() + temp - 2)
                    nextControlDate = dateNotUseful.strftime('%Y-%m-%d')
                if isinstance(temp, datetime.date):
                    nextControlDate = temp.strftime('%Y-%m-%d')
            except TypeError:
                print('Error en el sujeto: ' + dataFrame[headers[3]][i] +
                      '. El formato de fecha del último control es diferente al del resto del documento')
                print('Tipo de dato: ' + str(type(temp)))
            # print(nextControlDate, type(nextControlDate), 'should be str')

            # controlStatus
            temp = dataFrame[headers[60]][i]
            if pd.isnull(temp):
                controlStatus = None
            elif isinstance(temp, str):
                controlStatus = temp
            # print(controlStatus, type(controlStatus), 'should be str')

            # Comment
            # unregistered

            # PESO
            temp = dataFrame[headers[29]][i]
            if pd.isnull(temp):
                peso = -1.0
            elif isinstance(temp, float):
                peso = temp
            # print(peso, type(peso), 'should be float')

            # IMC
            temp = dataFrame[headers[31]][i]
            if pd.isnull(temp):
                imc = -1.0
            elif isinstance(temp, float) and not math.isnan(temp):
                imc = np.round(temp, decimals=2)
            # print(imc, type(imc), 'should be float')

            # nutrionalStatus
            # unregistered

            # RCV
            temp = dataFrame[headers[27]][i]
            if pd.isnull(temp):
                rcv = None
            else:
                if isinstance(temp, np.int64) and temp == 1:
                    rcv = 'BAJO'
                if isinstance(temp, np.int64) and temp == 2:
                    rcv = 'MODERADO'
                if isinstance(temp, np.int64) and temp == 3:
                    rcv = 'ALTO'
            # print(rcv, type(rcv), 'should be str')

            # DM
            temp = dataFrame[headers[17]][i]
            if pd.isnull(temp):
                dm = 0
            if isinstance(temp, np.int64) and temp == 1:
                dm = 1
            if isinstance(temp, np.int64) and temp == 2:
                dm = 0
            # print(dm, type(dm), 'should be int')

            # HTA
            temp = dataFrame[headers[16]][i]
            if pd.isnull(temp):
                hta = 0
            if isinstance(temp, np.int64) and temp == 1:
                hta = 1
            if isinstance(temp, np.int64) and temp == 2:
                hta = 0
            # print(hta, type(hta), 'should be int')

            # EPI
            temp = dataFrame[headers[21]][i]
            if pd.isnull(temp):
                age = 0
            else:
                if isinstance(temp, np.int64) and temp == 1:
                    epi = 1
                if isinstance(temp, np.int64) and temp == 2:
                    epi = 0
            # print(epi, type(epi), 'should be int')

            # DLP
            temp = dataFrame[headers[19]][i]
            if pd.isnull(temp):
                dlp = 0
            if isinstance(temp, np.int64) and temp == 1:
                dlp = 1
            if isinstance(temp, np.int64) and temp == 2:
                dlp = 0
            # print(dlp, type(dlp), 'should be int')

            # TABACO
            temp = dataFrame[headers[24]][i]
            if pd.isnull(temp):
                tabaco = 0
            if isinstance(temp, np.int64) and temp == 1:
                tabaco = 1
            if isinstance(temp, np.int64) and temp == 2:
                tabaco = 0
            # print(tabaco, type(tabaco), 'should be int')

            # ARTROSIS
            temp = dataFrame[headers[23]][i]
            if pd.isnull(temp):
                artrosis = 0
            else:
                if isinstance(temp, np.int64) and temp == 1:
                    artrosis = 1
                if isinstance(temp, np.int64) and temp == 2:
                    artrosis = 0
            # print(artrosis, type(artrosis), 'should be int')

            # PARKINSON
            temp = dataFrame[headers[22]][i]
            if pd.isnull(temp):
                parkinson = 0
            if isinstance(temp, np.int64) and temp == 1:
                parkinson = 1
            if isinstance(temp, np.int64) and temp == 2:
                parkinson = 0
            # print(parkinson, type(parkinson), 'should be int')

            # HIPO
            temp = dataFrame[headers[20]][i]
            if pd.isnull(temp):
                hipo = 0
            else:
                if isinstance(temp, np.int64) and temp == 1:
                    hipo = 1
                if isinstance(temp, np.int64) and temp == 2:
                    hipo = 0
            # print(hipo, type(hipo), 'should be int')

            # INSULINA
            temp = dataFrame[headers[18]][i]
            if pd.isnull(temp):
                insulina = 0
            if isinstance(temp, np.int64) and temp == 1:
                insulina = 1
            if isinstance(temp, np.int64) and temp == 2:
                insulina = 0
            # print(insulina, type(insulina), 'should be int')

            # INTO GLU
            temp = dataFrame[headers[15]][i]
            if pd.isnull(temp):
                int_glu = 0
            if isinstance(temp, np.float64) and temp == 1:
                int_glu = 1
            if isinstance(temp, np.float64) and temp == 2:
                int_glu = 0
            # print(int_glu, type(int_glu), 'should be int')

            # retinopatia diabetica
            # unregistered

            # empamDate
            temp = dataFrame[headers[50]][i]
            if pd.isnull(temp):
                empamDate = '1900-01-01'
                efamStatus = 'NO VIGENTE'
            elif isinstance(temp, int):
                dateNotUseful = datetime.date.fromordinal(
                    datetime.date(1900, 1, 1).toordinal() + temp - 2)
                empamDate = dateNotUseful.strftime('%Y-%m-%d')
                # print(empamDate, type(empamDate), 'should be str')
                # efamStatus
                # can be calculated
                lastDate = dateNotUseful
                oneYear = datetime.date.today() - relativedelta(years=1)
                if (lastDate >= oneYear):
                    efamStatus = 'VIGENTE'
                else:
                    efamStatus = 'NO VIGENTE'
            # print(efamStatus, type(efamStatus), 'should be str')

            # functionalDiagnosis
            temp = dataFrame[headers[51]][i]
            if pd.isnull(temp):
                func_diag = None
            elif isinstance(temp, str):
                func_diag = temp
            # print(func_diag, type(func_diag), 'should be str')

            # hbgDate
            excel_hbg_date = dataFrame[headers[44]][i]
            if pd.isnull(excel_hbg_date):
                hbgDate = '1900-01-01'
            else:
                try:
                    if isinstance(excel_hbg_date, int):
                        hbgDateNotUseful = datetime.date.fromordinal(
                            datetime.date(1900, 1, 1).toordinal() + excel_hbg_date - 2)
                        hbgDate = hbgDateNotUseful.strftime('%Y-%m-%d')
                    if isinstance(excel_hbg_date, datetime.date):
                        hbgDate = excel_hbg_date.strftime('%Y-%m-%d')
                    if isinstance(excel_hbg_date, str):
                        hbgDate = '1900-01-01'
                except TypeError:
                    print('Error en el sujeto: ' + dataFrame[headers[3]][i] +
                          '. El formato de fecha es diferente al del resto del documento')
            # print(hbgDate, type(hbgDate), 'should be str')

            # Hemoglobina glicosilada
            temp = dataFrame[headers[45]][i]
            if pd.isnull(temp):
                hbg = -1.0
            elif isinstance(temp, float):
                hbg = temp
            elif isinstance(temp, int):
                hbg = float(temp)
            # print(hbg, type(hbg), 'should be float')

            # cholesterolDate
            # only mena, cholesterol date equals to examination date
            # examinationDate
            excel_examination_date = dataFrame[headers[34]][i]
            if pd.isnull(excel_examination_date):
                examinationDate = '1900-01-01'
            else:
                try:
                    if isinstance(excel_examination_date, int):
                        examinationDateNotUseful = datetime.date.fromordinal(
                            datetime.date(1900, 1, 1).toordinal() + excel_examination_date - 2)
                        examinationDate = examinationDateNotUseful.strftime('%Y-%m-%d')
                    if isinstance(excel_examination_date, datetime.date):
                        examinationDate = excel_examination_date.strftime('%Y-%m-%d')
                    if isinstance(excel_examination_date, str):
                        # _examinationDate = excel_examination_date.replace('-', '/').replace(',', '/').replace('*', '')
                        examinationDate = '1900-01-01'
                except TypeError:
                    print('Error en el sujeto: ' + dataFrame[headers[3]][i] +
                          '. El formato de fecha es diferente al del resto del documento')
            colDate = examinationDate
            creaDate = examinationDate

            # CholesterolStatus
            # can be calculated
            lastDate = examinationDateNotUseful
            oneYear = datetime.date.today() - relativedelta(years=1)
            if (lastDate >= oneYear):
                colStatus = 'VIGENTE'
                creaStatus = 'VIGENTE'
            else:
                colStatus = 'NO VIGENTE'
                creaStatus = 'NO VIGENTE'
            # print(colStatus, type(colStatus), 'should be str')

            # Cholesterol
            temp = dataFrame[headers[35]][i]
            if pd.isnull(temp):
                col = -1.0
                colStatus = 'NO VIGENTE'
            else:
                if isinstance(temp, float):
                    col = temp
            # print(col, type(col), 'should be float')

            # LDL
            temp = dataFrame[headers[37]][i]
            if pd.isnull(temp) or isinstance(temp, str):
                ldl = -1.0
            else:
                if isinstance(temp, int):
                    if isinstance(temp, int):
                        if temp >= 2000:
                            date_temp = temp
                            ldl = -1.0
                        else:
                            ldl = float(temp)
                if isinstance(temp, float):
                    ldl = temp
            # print(ldl, type(ldl), 'should be float')

            # HDL
            temp = dataFrame[headers[36]][i]
            if isinstance(temp, str) or pd.isnull(temp):
                hdl = -1.0
            else:
                if isinstance(temp, int):
                    if isinstance(temp, int):
                        if temp >= 2000:
                            date_temp = temp
                            hdl = -1.0
                        else:
                            hdl = float(temp)
                if isinstance(temp, float) and not math.isnan(temp):
                    hdl = temp
            # print(hdl, type(hdl), 'should be float')

            # TGC
            temp = dataFrame[headers[38]][i]
            if isinstance(temp, str) or pd.isnull(temp):
                tgc = -1.0
            else:
                if isinstance(temp, int):
                    if isinstance(temp, int):
                        if temp >= 2000:
                            date_temp = temp
                            tgc = -1.0
                        else:
                            tgc = float(temp)
                if isinstance(temp, float):
                    tgc = temp
            # print(ldl, type(ldl), 'should be float')

            # EKGDate
            temp = dataFrame[headers[48]][i]
            if pd.isnull(temp):
                ekgDate = '1900-01-01'
                ekgStatus = 'NO VIGENTE'
            elif isinstance(temp, float):
                ekgDateNotUseful = datetime.date.fromordinal(
                    datetime.date(1900, 1, 1).toordinal() + int(temp) - 2)
                ekgDate = ekgDateNotUseful.strftime('%Y-%m-%d')
                # ekgStatus
                # can be calculated
                lastDate = ekgDateNotUseful
                oneYear = datetime.date.today() - relativedelta(years=1)
                if (lastDate >= oneYear):
                    ekgStatus = 'VIGENTE'
                else:
                    ekgStatus = 'NO VIGENTE'
            # print(ekgStatus, type(ekgStatus), 'should be str')

            # Creatinina
            temp = dataFrame[headers[40]][i]
            if isinstance(temp, str) or pd.isnull(temp):
                crea = -1.0
                creaStatus = 'NO VIGENTE'
            else:
                if isinstance(temp, int):
                    if isinstance(temp, int):
                        if temp >= 2000:
                            date_temp = temp
                            crea = -1.0
                            creaStatus = 'NO VIGENTE'
                        else:
                            crea = float(temp)
                if isinstance(temp, float):
                    crea = temp
            # print(crea, type(crea), 'should be float')

            # MICRO
            temp = dataFrame[headers[43]][i]
            if pd.isnull(temp):
                micro = -1.0
            else:
                if isinstance(temp, str):
                    try:
                        _temp = temp.split('>')
                        micro = float(_temp[1])
                    except:
                        micro = -1.0
                if isinstance(temp, datetime.date):
                    micro = -1.0
                if isinstance(temp, int):
                    if temp >= 2000:
                        date_temp = temp
                        micro = -1.0
                    else:
                        micro = float(temp)
                elif isinstance(temp, float):
                    micro = temp
            # print(micro, type(micro), 'should be float')

            # Glicemia
            temp = dataFrame[headers[39]][i]
            if isinstance(temp, str) or pd.isnull(temp):
                glic = -1.0
            elif isinstance(temp, int):
                glic = float(temp)
            elif isinstance(temp, float) and not math.isnan(temp):
                glic = temp
            # print(glic, type(glic), 'should be float')

            # RAC date
            temp = dataFrame[headers[46]][i]
            if pd.isnull(temp):
                racDate = '1900-01-01'
                racStatus = 'NO VIGENTE'
            else:
                try:
                    if isinstance(temp, int):
                        RacDateNotUseful = datetime.date.fromordinal(
                            datetime.date(1900, 1, 1).toordinal() + temp - 2)
                        racDate = RacDateNotUseful.strftime('%Y-%m-%d')
                        # ekgStatus
                        # can be calculated
                        lastDate = RacDateNotUseful
                        oneYear = datetime.date.today() - relativedelta(years=1)
                        if (lastDate >= oneYear):
                            racStatus = 'VIGENTE'
                        else:
                            racStatus = 'NO VIGENTE'
                    if isinstance(temp, datetime.date):
                        racDate = temp.strftime('%Y-%m-%d')
                except:
                    racDate = '1900-01-01'
            # print(racDate, type(racDate), 'should be str')
            # print(racStatus, type(racStatus), 'should be str')

            # RAC
            temp = dataFrame[headers[47]][i]
            if pd.isnull(temp):
                rac = -1.0
            elif isinstance(temp, float):
                rac = temp
            elif isinstance(temp, int):
                rac = float(temp)
            # print(rac, type(rac), 'should be float')

            # PieDiabetico
            temp = dataFrame[headers[55]][i]
            if pd.isnull(temp):
                pie = None
            elif isinstance(temp, str):
                pie = temp
            # print(pie, type(pie), 'should be str')

            # Fecha pieDiabetico
            temp = dataFrame[headers[54]][i]
            if pd.isnull(temp):
                pieDate = '1990-01-01'
                pieStatus = 'NO VIGENTE'
            else:
                try:
                    if isinstance(temp, int):
                        pieDateNotUseful = datetime.date.fromordinal(
                            datetime.date(1900, 1, 1).toordinal() + temp - 2)
                        pieDate = pieDateNotUseful.strftime('%Y-%m-%d')
                    if isinstance(temp, datetime.date):
                        pieDate = temp.strftime('%Y-%m-%d')
                    # ekgStatus
                    # can be calculated
                    lastDate = pieDateNotUseful
                    oneYear = datetime.date.today() - relativedelta(years=1)
                    if (lastDate >= oneYear):
                        pieStatus = 'VIGENTE'
                    else:
                        pieStatus = 'NO VIGENTE'
                except:
                    pieDate = '1990-01-01'
            # print(pieDate, type(pieDate), 'should be str')
            # print(pieStatus, type(pieStatus), 'should be str')

            # Podologia
            temp = dataFrame[headers[56]][i]
            if pd.isnull(temp):
                podoDate = '1990-01-01'
                podo = 'NO'
            else:
                try:
                    if isinstance(temp, int):
                        podoDateNotUseful = datetime.date.fromordinal(
                            datetime.date(1900, 1, 1).toordinal() + temp - 2)
                        podoDate = podoDateNotUseful.strftime('%Y-%m-%d')
                        podo = 'SI'
                    if isinstance(temp, datetime.date):
                        podoDate = temp.strftime('%Y-%m-%d')
                        podo = 'SI'
                    if isinstance(temp, str):
                        podoDate = '1990-01-01'
                        podo = 'NO'
                except:
                    podoDate = '1990-01-01'
            # print(podoDate, type(podoDate), 'should be str')

            # Presión Sistolica
            temp = dataFrame[headers[32]][i]
            if pd.isnull(temp):
                pSistolica = -1.0
            elif isinstance(temp, float):
                pSistolica = np.round(temp, decimals=2)
            # print(pSistolica, type(pSistolica), 'should be float')

            # Presión Diastolica
            temp = dataFrame[headers[33]][i]
            if pd.isnull(temp):
                pDiastolica = -1.0
            elif isinstance(temp, float):
                pDiastolica = temp
            # print(pDiastolica, type(pDiastolica), 'should be float')

            # hipoglicemiantes orales
            # unregistered

            # ecvs
            # unregistered

            # infarto
            temp = dataFrame[headers[26]][i]
            if pd.isnull(temp):
                infarto = 0
            else:
                if isinstance(temp, np.int64) and temp == 1:
                    infarto = 1
                if isinstance(temp, np.int64) and temp == 2:
                    infarto = 0
            # print(infarto, type(infarto), 'should be int')

            # aspirina
            temp = dataFrame[headers[57]][i]
            if pd.isnull(temp):
                aspirina = 0
            else:
                if isinstance(temp, float):
                    if temp == 1:
                        aspirina = 1
                    elif temp == 2:
                        aspirina = 0
            # print(aspirina, type(aspirina), 'should be int')

            # estatinas
            temp = dataFrame[headers[58]][i]
            if pd.isnull(temp):
                estatinas = 0
            elif isinstance(temp, float):
                if temp == 1:
                    estatinas = 1
                elif temp == 2:
                    estatinas = 0
            # print(estatinas, type(estatinas), 'should be int')

            # ieca
            # unregistered

            # sospecha maltrato
            # unregistered

            # actividad fisica
            # unregistered

            # VFG
            temp = dataFrame[headers[49]][i]
            if pd.isnull(temp):
                vfg = -1.0
            elif isinstance(temp, float):
                vfg = temp
            # print(vfg, type(vfg), 'should be float')

            #insulinoTerapia
            # unregistered

            #tug
            # unregistered

            #testUnipodal
            # unregistered

            #glicemiaAyuno
            # unregistered

            # vigencia
            temp = dataFrame[headers[60]][i]
            if pd.isnull(temp):
                vigencia = None
            elif isinstance(temp, str):
                vigencia = temp

            data = {
                'pscv': {
                    'cod': i,
                    'rut': doc + '-' + verifyingDigit,
                    'nombreCompleto': fullName,
                    'ficha': file,
                    'fechaNacimiento': birthDate,
                    'edad': age,
                    'sexo': sex,
                    'sector': sector,
                    'fechaIngreso': admissionDate,
                    'migrante': migrant,
                    'pueblosOriginarios': pOriginarios,
                    'fechaUltimoControl': lastControlDate,
                    'fechaProximoControl': nextControlDate,
                    'estadoControl': controlStatus,
                    'Comentario': comment,
                    'Nutricion': {
                        'imc': imc,
                        'peso': peso,
                        'estadoNutricional': nutrionalStatus
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
                        'estadoEfam': efamStatus,
                        'diagnosticoFuncional': func_diag
                    },
                    'examenes': {
                        'fechaExamenes': examinationDate,
                        'hemoglobinaGlicosilada': {
                            'Hba1c': hbg,
                            'fechaHemoglobinaGlicosilada': hbgDate
                        },
                        'colesterol': {
                            'fechaColesterol': colDate,
                            'estadoColesterol': colStatus,
                            'colesterolTotal': col,
                        },
                        'ldl': ldl,
                        'hdl': hdl,
                        'trigliceridos': tgc,
                        'ekg': {
                            'fechaEkg': ekgDate,
                            'estado': ekgStatus
                        },
                        'creatinina': {
                            'resultadoCreatinina': crea,
                            'estadoCreatinina': creaStatus,
                            'fechaCreatinina': creaDate
                        },
                        'microalbuminuria': micro,
                        'glicemia': glic,
                        'rac': {
                            'fechaRac': racDate,
                            'resultadoRac': rac,
                            'estadoRac': racStatus
                        },
                        'pieDiabetico': {
                            'fechaPieDiabetico': pieDate,
                            'estadoPieDiabetico': pieStatus,
                            'resultado': pie
                        },
                        'podologo': {
                            'examen': podo,
                            'fechaPodologo': podoDate,
                        },
                        'presion': {
                            'presionSistolica': pSistolica,
                            'presionDiastolica': pDiastolica,
                        },
                        'hipoglicemiantes orales': hipo_or,
                        'antecedentes': {
                            'ecvs': ecvs,
                            'infarto': infarto
                        },
                        'tratamientos': {
                            'aspirina': aspirina,
                            'estatinas': estatinas,
                            'IECA': ieca
                        },
                        'sospechaMaltrato': sospecha,
                        'actividadFisica': act_fisica,
                        'VFG': vfg,
                        'insulinoterapia': insulino_ter,
                        'tug': tug,
                        'testUnipodal': testUni,
                        'glicemiaAyunoAlterada': glicAyuno
                    },
                },
            }
        print(data)
        print(counter)

        destinationCollection.insert_one(data)
        print('-----------------------')

        print('success')
