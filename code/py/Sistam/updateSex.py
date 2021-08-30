import pymongo
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta


def updateSex(dataDoc, newSex):
    query = {'informacionPersonal.datosPersonales.documento.numero': dataDoc}
    newValues = {'$set': {'informacionPersonal.datosPersonales.genero': newSex}}
    collection.update_one(query, newValues)

    print('updating user: ', dataDoc)


if __name__ == '__main__':
    counter = 0
    #
    # Note: this script only works with pymongo 3.8
    client = pymongo.MongoClient("mongodb://localhost:27017/")

    db = client['demo']

    collection = db['personasContingencia']

    for i in range(0, 13):  # 128336 personas en db
        c = i * 10000

        a = 0 + c
        b = 10000

        print('start', a)

        for u in collection.find():

            if u is not None:

                counter += 1
                dataDoc = u['informacionPersonal']['datosPersonales']['documento']['numero']
                dataSex = u['informacionPersonal']['datosPersonales']['genero']

                if dataSex == 'MASCULINO':
                    newSex = 'masculino'

                    updateSex(dataDoc, newSex)
                    counter += 1

                elif dataSex == 'FEMENINO':
                    newSex = 'femenino'

                    updateSex(dataDoc, newSex)
                    counter += 1

    print(counter)
    print('success')
