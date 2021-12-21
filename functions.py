import requests
import xmltodict, json
import pyodbc
import pandas as pd
import sqlalchemy
import config

class XmlManipulator():
    def __init__(self, url, outerField):
    
        self.url = url
        self.outerField = outerField
        response_API = requests.get(url)

        if not response_API.ok:
            raise Exception("Api error")
        
        try:
            self.obj = xmltodict.parse(response_API.text)
        except Exception as e:
            raise Exception("Xml to json parse error "+ str(e))

        try: 
            for i in self.outerField:
                self.obj = self.obj[i]
        except Exception as e:
            raise Exception("Outer field error you may didnt give the outerfield by order plss check "+ str(e))


        database_con = config.CONNECTIONSTRING
        self.engine = sqlalchemy.create_engine(database_con)


    def getRawData(self):
        return self.obj

    def changeFieldValue(self, jsonData, fieldName, separator,indices):
        try: 
            for c,j in enumerate(fieldName):
                for count,i in enumerate(jsonData):
                    category = i[j].split(separator[c])
                    if indices[c] == "first":
                        category = category[0]
                    elif indices[c] == "last":
                        category = category[-1]
                    elif indices[c] == "firstAndLast":
                        category = category[0] +" > "+category[-1]
                    else:
                        category = category[0]

                    jsonData[count][j] = category

            return jsonData
        except Exception as e:
            print('changeFiedValue error: '+ str(e))

    def saveTxt(self, jsonData, fileName):
        try:
            with open(fileName, 'w') as f:
                json.dump(jsonData, f)
        except Exception as e:
            print('saveTxt error: '+ str(e))

    def jsonToDataFrame(self,jsonData):
        try:
            df = pd.json_normalize(jsonData)
            return df
        except Exception as e:
            print('jsonToDataFrame error: '+ str(e))

    def saveSql(self, df, tableName):
        try:
            df.to_sql(tableName,self.engine, if_exists="replace", method=None, chunksize=20)
        except:
            print('savesql error: '+ str(e))
       