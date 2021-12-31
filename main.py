import requests
import xmltodict, json
from time import sleep
import functions
import config
import pandas as pd

while(1):
    XmlManipulator = functions.XmlManipulator(config.URL,config.OUTERFIELDS)
    jsonData = XmlManipulator.getRawData()
    jsonData = XmlManipulator.changeFieldValue(jsonData, config.FIELDNAMES, config.SEPARATORS, config.INDIES)


    if config.CREATERELATEDTABLE:
        XmlManipulator.createTable(jsonData)

    df = XmlManipulator.jsonToDataFrame(jsonData)

    if config.ROWTOSTR:
        for j in df.columns:
            for c,i in enumerate(df[j]):
                df[j][c] = str(i)
    if config.SAVEASTXT:
        XmlManipulator.saveTxt(jsonData, config.TXTNAME)

    if config.SEOCOL:
        df['seo'] = df.apply(lambda row: str(XmlManipulator.cleanSeo(row.urunismi))+"-"+str(row.id), axis=1)
    if config.SAVEASSQL:
        XmlManipulator.saveSql(df, config.TABLENAME)

    if config.EXTRATABLE:
        extra_df = XmlManipulator.extraTable(df)
        extra_df['seo'] = extra_df.apply(lambda row: str(XmlManipulator.cleanSeo(row.kategori_ismi)), axis=1)
        XmlManipulator.saveSql(extra_df, config.EXTRATABLENAME)


    print(df.head(10))
    print("#############################################################################################################################")

    sleep(config.TIME)
