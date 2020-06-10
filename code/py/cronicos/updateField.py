import pymongo

if __name__ == '__main__':
    counter = 0
    # Note: this script only works with pymongo 3.8
    client = pymongo.MongoClient("mongodb://localhost:27017/")

    db = client['demo']

    collection = db['personasContingencia']

    for u in collection.find():
        if u is not None:
            query = {'diabetes': {'$exists': False}}
            # query = {'institucion': {'$exists': False}}

            result = collection.find_one(query)

            if result:
                counter += 1

                newValues = {
                    '$set': {
                        'diabetes': False,
                        'hipertension': False,
                        'dislipidemia': False,
                        'tabaco': False,
                        'artrosis': False,
                        'parkinson': False,
                        'hipotiroidismo': False,
                        'epilepsia': False,
                        'glaucoma': False,
                    }
                }
                """
                newValues = {
                    '$set': {
                        'institucion':
                            {
                                'cormuval': True
                            }
                    }
                }
                """
                print('updating:', counter)
                collection.update_one(query, newValues)
