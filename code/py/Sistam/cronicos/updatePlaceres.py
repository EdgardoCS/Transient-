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

    path = os.path.join(Path('placeres.xlsx'))
    dataFrame = pd.read_excel('placeres.xlsx', sheet_name='Hoja2')

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
        temp = dataFrame[headers[2]][i]
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
                temp = dataFrame[headers[10]][i]
                if isinstance(temp, str) and temp == 'DM':
                    diabetes = True
                else:
                    diabetes = False

                'Hipertensión Arterial'
                temp = dataFrame[headers[9]][i]
                if isinstance(temp, str) and temp == 'HTA':
                    hipertension = True
                else:
                    hipertension = False

                'Dislipidemia'
                temp = dataFrame[headers[11]][i]
                if isinstance(temp, str) and temp == 'DLP':
                    dislipidemia = True
                else:
                    dislipidemia = False

                'Hipotiroidismo'
                temp = dataFrame[headers[12]][i]
                if isinstance(temp, str) and temp == 'HIPO':
                    hipotiroidismo = True
                else:
                    hipotiroidismo = False

                'Artrosis'
                temp = dataFrame[headers[15]][i]
                if isinstance(temp, str) and temp == 'ARTROSIS':
                    artrosis = True
                else:
                    artrosis = False

                'Epilepsia'
                temp = dataFrame[headers[13]][i]
                if isinstance(temp, str) and temp == 'EPI':
                    epilepsia = True
                else:
                    epilepsia = False

                'Tabaquismo'
                temp = dataFrame[headers[18]][i]
                if isinstance(temp, str) and temp == 'POSITIVO':
                    tabaco = True
                else:
                    tabaco = False

                'Parkinson'
                temp = dataFrame[headers[17]][i]
                if isinstance(temp, str) and temp == 'PARKINSON':
                    parkinson = True
                else:
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
