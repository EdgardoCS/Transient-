import os
import json
import time
import math
import pymongo
import datetime
import numpy as np
import pandas as pd
from pathlib import Path

if __name__ == '__main__':
    """
    # Note: this script only works with pymongo 3.8

    client = pymongo.MongoClient("mongodb://localhost:27017/")

    db = client[""]

    destinationCollection = db["full-pscv-mena"]
    """

    path = os.path.join(Path('C:/Users/Ed/Documents/'),
                        'PNUD/Producto7/Planillas/PLANILLA_INGRESO - Río Hurtado v1.xlsx')

    dataFrame = pd.read_excel(path, sheet_name='Gts Territorial')
    headers = dataFrame.columns

    counter = 0
    featureCollection = []

    for i in range(0, len(dataFrame)):
        name = None  # string
        lastName = None  # string
        rut = None  # int
        birthDate = None  # date
        sex = None  # string
        phone = None  # int
        mail = None  # string
        region = None  # string
        city = None  # string

        counter += 1

        temp = dataFrame[headers[0]][i]
        if isinstance(temp, str):
            name = temp

        temp = dataFrame[headers[1]][i]
        if isinstance(temp, str):
            lastName = temp

        temp = dataFrame[headers[2]][i]
        if temp is not None:
            rut = temp

        temp = dataFrame[headers[3]][i]
        birthDate = temp.strftime('%Y-%m-%d')

        temp = dataFrame[headers[4]][i]
        if isinstance(temp, str):
            sex = temp

        temp = dataFrame[headers[5]][i]
        if isinstance(temp, np.int64):
            phone = int(temp)

        temp = dataFrame[headers[6]][i]
        if isinstance(temp, str):
            mail = temp

        temp = dataFrame[headers[7]][i]
        if isinstance(temp, str):
            region = temp

        temp = dataFrame[headers[8]][i]
        if isinstance(temp, str):
            city = temp

        features = {
            "role": "Gestor",
            'rut': rut,
            'nombres': name,
            'apellidos': lastName,
            'fechaNacimiento': birthDate,
            'sexo': sex,
            'telefono': phone,
            'region': region,
            'comuna': city,
            'email': mail,
        }

        # print(object_name)
        featureCollection.append(features)

    with open('dataGestores.json', 'w', encoding='utf8') as json_file:
        json.dump(featureCollection, json_file, ensure_ascii=False)
        json_file.close()
