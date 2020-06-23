import pymongo
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta


def updateCoordinates(dataDoc, coordinates):
    query = {'informacionPersonal.datosPersonales.documento.numero': dataDoc}

    newValues = {'$set': {'informacionPersonal.geometry.coordinates': coordinates}}
    collection.update_one(query, newValues)

    print('updated user: ', dataDoc)


if __name__ == '__main__':
    counter = 0
    #
    # Note: this script only works with pymongo 3.8
    client = pymongo.MongoClient("mongodb://localhost:27017/")

    db = client['demo']

    collection = db['personasContingencia']

    for u in collection.find():

        if u is not None:

            dataDoc = u['informacionPersonal']['datosPersonales']['documento']['numero']
            dataInstitucion = u['institucion']
            dataCesfam = u['informacionPersonal']['informacionFamiliar']['cesfam']
            dataCoordinates = u['informacionPersonal']['geometry']['coordinates']

            if dataInstitucion == {'loncoche': True}:

                if dataCesfam is not None and dataCesfam == 'huiscapi':
                    if dataCoordinates == [0.0, 0.0]:
                        coordinates = [-72.40598824695050, -39.2965257140425]
                        counter += 1
                        updateCoordinates(dataDoc, coordinates)
                elif dataCesfam is not None and dataCesfam == 'la paz':
                    if dataCoordinates == [0.0, 0.0]:
                        coordinates = [-72.7132769784926, -39.4101401762003]
                        counter += 1
                        updateCoordinates(dataDoc, coordinates)
    print(counter)
    print('success')
