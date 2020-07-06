"""
Cambiar direcciones a minuscula
y cambiar maestro de calles a minuscula
"""

import pymongo


def updateMaster(dataInstitucion, newMaster):
    query = {'institucion': dataInstitucion}

    newValues = {
        '$set':
            {
                'maestroCalles': newMaster,
            }
    }
    collection.update_one(query, newValues)


if __name__ == '__main__':
    counter = 0

    # Note: this script only works with pymongo 3.8
    client = pymongo.MongoClient("mongodb://localhost:27017/")

    db = client['demo']

    collection = db['clients']

    newMaster = []

    for u in collection.find():

        if u is not None:
            dataInstitucion = u['institucion']
            dataMaster = u['maestroCalles']

            newMaster = []

            if dataInstitucion == 'loncoche':
                for x in dataMaster:
                    newMaster.append(x.lower())
                updateMaster(dataInstitucion, newMaster)

            elif dataInstitucion == 'cormuval':
                for x in dataMaster:
                    newMaster.append(x.lower())
                updateMaster(dataInstitucion, newMaster)

    print('success')
