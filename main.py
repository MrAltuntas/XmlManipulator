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


##########
    if config.CREATERELATEDTABLE:

        df_variant = pd.DataFrame()
        for c,i in enumerate(jsonData):
            if config.RELATEDFIELDNAME in i:
                test = i[config.RELATEDFIELDNAME]

                for x in config.RELATEDOUTERFIELDS:
                    test = test[x]

                temp_df = XmlManipulator.jsonToDataFrame(test)

                temp_df["uid"] = i["id"]

                df_variant = df_variant.append(temp_df, ignore_index=True) 

                del jsonData[c][config.RELATEDFIELDNAME]   
        
        if config.SAVEASSQL:
            XmlManipulator.saveSql(df_variant, config.RELATEDTABLENAME)

        print(df_variant.head(10))
##############


    df = XmlManipulator.jsonToDataFrame(jsonData)

    if config.ROWTOSTR:
        for j in df.columns:
            for c,i in enumerate(df[j]):
                df[j][c] = str(i)
    if config.SAVEASTXT:
        XmlManipulator.saveTxt(jsonData, config.TXTNAME)
    if config.SAVEASSQL:
        XmlManipulator.saveSql(df, config.TABLENAME)

    print(df.head(10))

    sleep(config.TIME)
