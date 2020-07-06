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

    # path = os.path.join(Path('/cordillera.xlsx'))
    dataFrame = pd.read_excel('cordillera.xlsx', sheet_name='Hoja1')

    headers = dataFrame.columns

    counter = 0
    totalCounter = 0

    diabetes = False
    hipertension = False
    dislipidemia = False
    tabaco = False
    artrosis = False
    parkinson = False
    hipotiroidismo = False
    epilepsia = False
    glaucoma = False

    for i in range(0, len(dataFrame)):
        temp = dataFrame[headers[3]][i]
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

                'PATOLOGIAS '
                temp = dataFrame[headers[10]][i]
                if isinstance(temp, str):
                    if temp == 'HIPO':
                        hipotiroidismo = True
                    else:
                        hipotiroidismo = False

                    if temp == 'DISLIPIDEMIA':
                        dislipidemia = True
                    else:
                        dislipidemia = False

                    if temp == 'HTA':
                        hipertension = True
                    else:
                        hipertension = False

                    if temp == 'DM':
                        diabetes = True
                    else:
                        diabetes = False

                    if temp == 'MIXTO':
                        diabetes = True
                        hipertension = True
                    else:
                        diabetes = False
                        hipertension = False

                    if temp == 'ARTROSIS':
                        artrosis = True
                    else:
                        artrosis = False

                    if temp == 'EPI':
                        epilepsia = True
                    else:
                        epilepsia = False

                    if temp == 'PARKINSON':
                        parkinson = True
                    else:
                        parkinson = False

                'Tabaquismo'
                temp = dataFrame[headers[21]][i]
                if isinstance(temp, str) and temp == 'SI':
                    tabaco = True
                elif isinstance(temp, str) and temp == 'NO':
                    tabaco = False

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
                print('updating:', counter)
                collection.update_one(query, newValues)

print(counter, 'actualizados, de un total de:', totalCounter)
