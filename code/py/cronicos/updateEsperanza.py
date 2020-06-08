import os
import math
import pymongo
import numpy as np
import pandas as pd
from pathlib import Path

if __name__ == '__main__':
    counter = 0
    ##
    # Note: this script only works with pymongo 3.8
    client = pymongo.MongoClient("mongodb://localhost:27017/")

    db = client['demo']

    #

    collection = db['personasContingencia']

    path = os.path.join(Path('/home/ed/Downloads/PLANILLA CV ESPERANZA.xlsx'))
    dataFrame = pd.read_excel(path, sheet_name='Sheet1')

    headers = dataFrame.columns

    counter = 0
    totalCounter = 0

    diabetes = None
    hipertension = None
    dislipidemia = None
    tabaco = None
    artrosis = None
    parkinson = None
    hipotiroidismo = None
    epilepsia = None
    glaucoma = None

    for i in range(0, len(dataFrame)):
        temp = dataFrame[headers[16]][i]
        if isinstance(temp, str):
            tempRut = temp.split('-')

            if len(tempRut) > 1:
                docType = 'rut'
                doc = tempRut[0].strip()
                digit = tempRut[1].strip()

        if doc:
            totalCounter += 1
            query = {'informacionPersonal.datosPersonales.documento.numero': doc}
            result = collection.find_one(query)

            if result:
                print(doc)
                counter += 1

                'Diabetes Mellitus'
                temp = dataFrame[headers[8]][i]
                if isinstance(temp, str):
                    if 'n' in temp or 'N' in temp:
                        diabetes = False
                    elif 's' in temp or 'S' in temp:
                        diabetes = True

                'Hipertensión Arterial'
                temp = dataFrame[headers[9]][i]
                if isinstance(temp, str):
                    if 'n' in temp or 'N' in temp:
                        hipertension = False
                    elif 's' in temp or 'S' in temp:
                        hipertension = True

                'Hipotiroidismo'
                temp = dataFrame[headers[10]][i]
                if isinstance(temp, str):
                    if 'n' in temp or 'N' in temp:
                        hipotiroidismo = False
                    elif 's' in temp or 'S' in temp:
                        hipotiroidismo = True

                'Artrosis'
                temp = dataFrame[headers[11]][i]
                if isinstance(temp, str):
                    if 'n' in temp or 'N' in temp:
                        artrosis = False
                    elif 's' in temp or 'S' in temp:
                        artrosis = True

                'Epilepsia'
                temp = dataFrame[headers[12]][i]
                if isinstance(temp, str):
                    if 'n' in temp or 'N' in temp:
                        epilepsia = False
                    elif 's' in temp or 'S' in temp:
                        epilepsia = True

                'Tabaquismo'
                temp = dataFrame[headers[35]][i]
                if isinstance(temp, str):
                    if 'n' in temp or 'N' in temp:
                        tabaco = False
                    elif 's' in temp or 'S' in temp:
                        tabaco = True

                'Parkinson'
                temp = dataFrame[headers[13]][i]
                if isinstance(temp, str):
                    if 'n' in temp or 'N' in temp:
                        parkinson = False
                    elif 's' in temp or 'S' in temp:
                        parkinson = True

                'Glaucoma'

                newValues = {
                    '$set': {
                        'diabetes': diabetes,
                        'hipertension': hipertension,
                        'dislipidemia': dislipidemia,
                        'tabaco': tabaco,
                        'artrosis': artrosis,
                        'parkinson': parkinson,
                        'hipotiroidismo': hipotiroidismo,
                        'epilepsia': epilepsia,
                        'glaucoma': glaucoma,

                    }
                }
                # collection.update_one(query, newValues)

print(counter, 'actualizados, de un total de: ', totalCounter)
