import requests
import xmltodict, json
from time import sleep
import functions
import config


while(1):
    XmlManipulator = functions.XmlManipulator(config.URL,config.OUTERFIELDS)
    jsonData = XmlManipulator.getRawData()
    jsonData = XmlManipulator.changeFieldValue(jsonData, config.FIELDNAMES, config.SEPARATORS, config.INDIES)
    df = XmlManipulator.jsonToDataFrame(jsonData)

    for c,i in enumerate(df['resimler.resim']):
        df['resimler.resim'][c] = str(i)

    if config.SAVEASTXT:
        XmlManipulator.saveTxt(jsonData)
    if config.SAVEASSQL:
        XmlManipulator.saveSql(df, config.TABLENAME)

    print(df.head(10))

    sleep(config.TIME)
