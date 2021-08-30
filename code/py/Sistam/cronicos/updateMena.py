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

    path = os.path.join(Path('/home/ed/Downloads/mena.xlsx'))
    dataFrame = pd.read_excel(path, sheet_name='TARJETERO')

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
                counter += 1

                'Diabetes Mellitus'
                temp = dataFrame[headers[17]][i]
                if isinstance(temp, np.int64) and temp == 1:
                    diabetes = True
                elif isinstance(temp, np.int64) and temp == 2:
                    diabetes = False

                'Hipertensión Arterial'
                temp = dataFrame[headers[16]][i]
                if isinstance(temp, np.int64) and temp == 1:
                    hipertension = True
                elif isinstance(temp, np.int64) and temp == 2:
                    hipertension = False

                'Dislipidemia'
                temp = dataFrame[headers[19]][i]
                if isinstance(temp, np.int64) and temp == 1:
                    dislipidemia = True
                elif isinstance(temp, np.int64) and temp == 2:
                    dislipidemia = False

                'Hipotiroidismo'
                temp = dataFrame[headers[20]][i]
                if isinstance(temp, np.int64) and temp == 1:
                    hipotiroidismo = True
                elif isinstance(temp, np.int64) and temp == 2:
                    hipotiroidismo = False

                'Artrosis'
                temp = dataFrame[headers[23]][i]
                if isinstance(temp, np.int64) and temp == 1:
                    artrosis = True
                elif isinstance(temp, np.int64) and temp == 2:
                    artrosis = False

                'Epilepsia'
                temp = dataFrame[headers[21]][i]
                if isinstance(temp, np.int64) and temp == 1:
                    epilepsia = True
                elif isinstance(temp, np.int64) and temp == 2:
                    epilepsia = False

                'Tabaquismo'
                temp = dataFrame[headers[24]][i]
                if isinstance(temp, np.int64) and temp == 1:
                    tabaco = True
                elif isinstance(temp, np.int64) and temp == 2:
                    tabaco = False

                'Parkinson'
                temp = dataFrame[headers[22]][i]
                if isinstance(temp, np.int64) and temp == 1:
                    parkinson = True
                elif isinstance(temp, np.int64) and temp == 2:
                    parkinson = False

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
