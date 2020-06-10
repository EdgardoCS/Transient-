import pymongo
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta

if __name__ == '__main__':
    counter = 0
    ##
    # Note: this script only works with pymongo 3.8
    client = pymongo.MongoClient("mongodb://localhost:27017/")

    db = client['demo']

    ##
    # MenaDb

    collection = db['pscvMenaFull']

    today = date.today()

    for u in collection.find():
        if u is not None:

            counter += 1
            dataDoc = u['pscv']['rut']
            dataAge = u['pscv']['edad']
            dataBirthDate = u['pscv']['fechaNacimiento']
            if dataBirthDate != '1990-01-01':
                rdelta = relativedelta(today, datetime.datetime.strptime(dataBirthDate, '%Y-%m-%d'))
                actualAge = rdelta.years
                if dataAge != actualAge:

                    #print('diferencia encontrada', dataAge, actualAge)

                    # Find patient using doc
                    query = {'pscv.rut': dataDoc}
                    result = collection.find_one(query)

                    newValues = {'$set': {'pscv.edad': actualAge}}
                    collection.update_one(query, newValues)

                    print('updated user: ', dataDoc)
    print('success')

