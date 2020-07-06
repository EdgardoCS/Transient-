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

    # path = os.path.join(Path('lasCanas.xls'))
    dataFrame = pd.read_excel('lasCanas.xls', sheet_name='Sheet1')

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
        temp = dataFrame[headers[0]][i]
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
                temp = dataFrame[headers[1]][i]
                if isinstance(temp, str) and temp == 'dm':
                    diabetes = True
                else:
                    diabetes = False

                'Hipertensión Arterial'
                if isinstance(temp, str) and temp == 'hta':
                    hipertension = True
                else:
                    hipertension = False

                'Dislipidemia'
                if isinstance(temp, str) and temp == 'disli':
                    dislipidemia = True
                else:
                    dislipidemia = False

                'Hipotiroidismo'
                if isinstance(temp, str) and temp == 'hipo':
                    hipotiroidismo = True
                else:
                    hipotiroidismo = False

                'Artrosis'
                if isinstance(temp, str) and temp == 'artrosis':
                    artrosis = True
                else:
                    artrosis = False

                'Epilepsia'
                if isinstance(temp, str) and temp == 'epi':
                    epilepsia = True
                else:
                    epilepsia = False

                'Tabaquismo'
                if isinstance(temp, str) and temp == 'tabaco':
                    tabaco = True
                else:
                    tabaco = False

                'Parkinson'
                if isinstance(temp, str) and temp == 'park':
                    parkinson = True
                else:
                    parkinson = False

                'Glaucoma'
                if isinstance(temp, str) and temp == 'glau':
                    glaucoma = True
                else:
                    glaucoma = False

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
