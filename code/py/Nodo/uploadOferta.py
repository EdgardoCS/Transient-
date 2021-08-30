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

    path = os.path.join(Path('C:/Users/Ed/Documents/'),
                        'PNUD/Producto7/Planillas/nuevo\Puren/PLANILLA_INGRESO1.xlsx')

    dataFrame = pd.read_excel(path, sheet_name='Oferta Programática')
    headers = dataFrame.columns

    counter = 0
    featureCollection = []

    for i in range(0, len(dataFrame)):
        title = None  # string
        body = None  # string
        startDate = None  # int
        endDate = None  # date
        institution = None  # string
        image = None  # int
        reach = None  # string
        region = None  # string
        city = None  # string
        type = None  # string
        keywords = None  # string

        counter += 1

        temp = dataFrame[headers[0]][i]
        if isinstance(temp, str):
            title = temp
        else:
            title = None

        temp = dataFrame[headers[1]][i]
        if isinstance(temp, str):
            body = temp
        else:
            body = None

        temp = dataFrame[headers[2]][i]
        startDate = temp.strftime('%Y-%m-%d')

        temp = dataFrame[headers[3]][i]
        endDate = temp.strftime('%Y-%m-%d')
        # endDate = temp

        temp = dataFrame[headers[4]][i]
        if isinstance(temp, str):
            institution = temp
        else:
            institution = None

        temp = dataFrame[headers[5]][i]
        print(temp)
        image = str(temp)
        if temp is None:
            image = "https://lh3.googleusercontent.com/On8XysUksgBd_pe6YNCJ7To2H6Beh2W2BfhvE6WocyJbRQi-woCiUaZw_IVd7X_fspQ88D9Lg_GSNPRIKsW5qGNCB4uhusorklxPJtfr-6-6oxlIn0BKyfEFBAS7p1EaC61_f-GF=w2400"

        temp = dataFrame[headers[6]][i]
        if isinstance(temp, str):
            if temp == 'SI':
                reach = True
            elif temp == 'Sí':
                reach = True
            elif temp == 'Si':
                reach = True
            else:
                reach = False
        else:
            reach = None

        temp = dataFrame[headers[7]][i]
        if isinstance(temp, str):
            if temp == 'Aysén del Gral. Carlos Ibánez del Campo':
                region = 'Aysén del General Carlos Ibánez del Campo'
            else:
                region = temp
        else:
            region = None

        temp = dataFrame[headers[8]][i]
        if isinstance(temp, str):
            city = temp
        else:
            city = None

        temp = dataFrame[headers[9]][i]
        if isinstance(temp, str):
            type = temp
        else:
            type = None

        temp = dataFrame[headers[10]][i]
        if isinstance(temp, str):
            tempKeyword = temp.split(", ")
            keywords = temp
        else:
            keywords = None

        features = {
            "entidad": institution,
            'isNacional': reach,
            'titulo': title,
            'cuerpo': body,
            'inicio': startDate,
            'termino': endDate,
            'imagenURL': image,
            'comuna': region,
            'region': city,
        }

        print(features)
        featureCollection.append(features)

    with open('dataOferta.json', 'w', encoding='utf8') as json_file:
        json.dump(featureCollection, json_file, ensure_ascii=False)
        json_file.close()
