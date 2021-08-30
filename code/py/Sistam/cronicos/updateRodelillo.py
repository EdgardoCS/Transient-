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
    collection = db['personasContingencia']

    path = os.path.join(Path('/home/ed/Downloads/rodelillo.xlsm'))
    dataFrame = pd.read_excel(path, sheet_name='Datos')

    headers = dataFrame.columns

    counter = 0
    totalCounter = 0

    doc = None

    diabetes = False
    hipertension = False
    dislipidemia = False
    tabaco = False
    artrosis = False
    parkinson = False
    hipotiroidismo = False
    epilepsia = False
    glaucoma = False

    for i in range(0, 4007):
        temp = dataFrame[headers[1]][i]

        if isinstance(temp, int):
            doc = temp

        totalCounter += 1

        query = {'informacionPersonal.datosPersonales.documento.numero': str(doc)}
        result = collection.find_one(query)

        if result:
            counter += 1

            'Diabetes && Hipertension'
            temp = dataFrame[headers[11]][i]
            if isinstance(temp, str) and temp == 'HTA':
                hipertension = True
            else:
                hipertension = False
            if isinstance(temp, str) and temp == 'DM':
                diabetes = True
            else:
                diabetes = False
            if isinstance(temp, str) and 'MIX' in temp:
                hipertension = True
                diabetes = True
            else:
                hipertension = False
                diabetes = False

            'Otras'
            temp = dataFrame[headers[32]][i]
            if isinstance(temp, str):
                if 'hipo' in temp or 'HIPO' in temp:
                    hipotiroidismo = True
                else: hipotiroidismo = False
                if 'DISL' in temp or 'Disl' in temp or 'DLP' in temp:
                    dislipidemia = True
                else:
                    dislipidemia = False
                if 'trosi' in temp or 'trosi' in temp or 'TROSI' in temp:
                    artrosis = True
                else:
                    artrosis = False
                if 'EPI' in temp or 'Epi' in temp:
                    epilepsia = True
                else: epilepsia = False
                if 'park' in temp or 'PARK' in temp or 'Park' in temp:
                    parkinson = True
                else:
                    parkinson = False

            'Tabaquismo'
            temp = dataFrame[headers[10]][i]
            if isinstance(temp, str) and temp == 'Negativo':
                tabaco = False
            elif isinstance(temp, str) and temp == 'Positivo':
                tabaco = True

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
            # print(newValues)
            print('updating:', counter)
            collection.update_one(query, newValues)

print(counter, 'actualizados, de un total de: ', totalCounter)
