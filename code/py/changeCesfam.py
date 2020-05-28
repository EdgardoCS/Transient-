import pymongo

if __name__ == '__main__':

    counter = 0
    ##
    # Note: this script only works with pymongo 3.8
    client = pymongo.MongoClient("mongodb://localhost:27017/")

    db = client['demo']

    ##
    collection = db['personasContingencia']

    cesfam = None

    quebradaVerde = ['Quebrada', 'quebrada', 'QUEBRADA']
    baron = ['Baron', 'baron', 'BARON']
    lasCañas = ['Cañas', 'Canas', 'cañas', 'canas', 'CAÑAS', 'CANAS']
    reinaIsabel = ['Isabel', 'isabel', 'ISABEL']
    rodelillo = ['Rodelillo', 'rodelillo', 'RODELILLO']
    placilla = ['Placilla', 'placilla', 'PLACILLA']
    padreDamian = ['Padre', 'padre', 'PADRE']
    mena = ['Mena', 'mena', 'MENA']
    cordillera = ['Cordillera', 'cordillera', 'CORDILLERA']
    placeres = ['Placeres', 'placeres', 'PLACERES']
    lagunaVerde = ['Laguna', 'laguna', 'LAGUNA']
    puertasNegras = ['Puertas', 'puertas', 'PUERTAS']
    esperanza = ['Esperanza', 'esperanza', 'ESPERANZA']

    user = collection.find({})
    for document in user:
        print(document)

        idCesfam = document['informacionPersonal']['informacionFamiliar']['cesfam']
        # if idCesfam == 'marcelo mena' or idCesfam == 'MARCELO MENA' or idCesfam == "CENTRO DE SALUD MARCELO MENA" or idCesfam == 'CESFAM MARCELO MENA' or idCesfam == 'cesfam marcelo mena':
        #    print(idCesfam)

        if any(x in idCesfam for x in mena):
            cesfam = 'marcelo mena'
        elif any(x in idCesfam for x in esperanza):
            cesfam = 'esperanza'
        elif any(x in idCesfam for x in rodelillo):
            cesfam = 'rodelillo'
        elif any(x in idCesfam for x in padreDamian):
            cesfam = 'padre damian de molokai'
        elif any(x in idCesfam for x in placeres):
            cesfam = 'placeres'
        elif any(x in idCesfam for x in quebradaVerde):
            cesfam = 'quebrada verde'
        elif any(x in idCesfam for x in baron):
            cesfam = 'baron'
        elif any(x in idCesfam for x in cordillera):
            cesfam = 'cordillera'
        elif any(x in idCesfam for x in lasCañas):
            cesfam = 'las cañas'
        elif any(x in idCesfam for x in reinaIsabel):
            cesfam = 'reina isabel II'
        elif any(x in idCesfam for x in placilla):
            cesfam = 'placilla'
        elif any(x in idCesfam for x in lagunaVerde):
            cesfam = 'laguna verde'
        elif any(x in idCesfam for x in puertasNegras):
            cesfam = 'puertas negras'

        counter += 1
        # newValues = {'$set': {'informacionPersonal.informacionFamiliar.cesfam': cesfam}}
        # collection.update_one(document, newValues)

        # print('updated user: ', counter)

print('-----------------------')
print('success')
