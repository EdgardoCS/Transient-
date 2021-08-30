"""
Cambiar direcciones a minuscula
y cambiar maestro de calles a minuscula
"""

import pymongo


def updateCaps(dataDoc, newStreet, newName, newLastName1, newLastName2):
    query = {'informacionPersonal.datosPersonales.documento.numero': dataDoc}

    newValues = {
        '$set':
            {
                'informacionPersonal.datosContacto.direccion.calle': newStreet,
                'informacionPersonal.datosPersonales.nombre': newName,
                'informacionPersonal.datosPersonales.apellido1': newLastName1,
                'informacionPersonal.datosPersonales.apellido2': newLastName2
            }
    }
    collection.update_one(query, newValues)

    print('updating user: ', dataDoc)


if __name__ == '__main__':
    counter = 0

    # Note: this script only works with pymongo 3.8
    client = pymongo.MongoClient("mongodb://localhost:27017/")

    db = client['demo']

    collection = db['personasContingencia']

    for u in collection.find():

        if u is not None:

            dataDoc = u['informacionPersonal']['datosPersonales']['documento']['numero']
            dataInstitucion = u['institucion']
            dataStreet = u['informacionPersonal']['datosContacto']['direccion']['calle']
            dataName = u['informacionPersonal']['datosPersonales']['nombre']
            dataLastName1 = u['informacionPersonal']['datosPersonales']['apellido1']
            dataLastName2 = u['informacionPersonal']['datosPersonales']['apellido2']

            if dataInstitucion == {'loncoche': True}:
                counter += 1

                if dataStreet.isupper():
                    newStreet = dataStreet.lower()
                else:
                    newStreet = dataStreet

                if dataName.isupper():
                    newName = dataName.lower()
                else:
                    newName = dataName

                if dataLastName1.isupper():
                    newLastName1 = dataLastName1.lower()
                else:
                    newLastName1 = dataLastName1

                if dataLastName2.isupper():
                    newLastName2 = dataLastName2.lower()
                else:
                    newLastName2 = dataLastName2

                updateCaps(dataDoc, newStreet, newName, newLastName1, newLastName2)

    print(counter)
    print('success')
