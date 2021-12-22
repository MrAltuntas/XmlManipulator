import requests
import xmltodict, json
import pyodbc
import pandas as pd
import sqlalchemy
import config
import re 

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

    def guaranteed_list(self,x):
        if not x:
            return []
        elif isinstance(x, list):
            return x
        else:
            return [x]

    def createTable(self, jsonData):
        for relatedFieldCounter,relatedField in enumerate(config.RELATEDFIELDNAME):
            #exec(df+"_"+relatedField+" = pd.DataFrame()")
            exec(f'df_{relatedField} = pd.DataFrame()')

            for c,i in enumerate(jsonData):
                if relatedField in i:
                    temp_json = i[relatedField]
                    for x in config.RELATEDOUTERFIELDS[relatedFieldCounter]:
                        temp_json = temp_json[x]

                    temp_df = self.jsonToDataFrame(self.guaranteed_list(temp_json))
                    temp_df["uid"] = i["id"]

                    #exec(df+"_"+relatedField+"") = exec(df+"_"+relatedField).append(temp_df, ignore_index=True)
                    exec(f'df_{relatedField} = df_{relatedField}.append(temp_df, ignore_index=True)')

                    del jsonData[c][relatedField]   

            if config.SAVEASSQL:
                #self.saveSql(exec(df+"_"+relatedField), config.RELATEDTABLENAME[relatedFieldCounter])
                exec(f'self.saveSql(df_{relatedField}, config.RELATEDTABLENAME[{relatedFieldCounter}])')

            #print(exec(df+"_"+relatedField))
            exec(f'print(df_{relatedField}.head(10))')

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

    def cleanSeo(self, data):
        try:
            data = data.lower()
            data = data.replace(" ", "-")
            data = data.replace("ı", "i")
            data = data.replace("ş", "s")
            data = data.replace("ö", "o")
            data = data.replace("ü", "u")
            data = data.replace("ğ", "g")
            data = data.replace("ç", "c")
            data = re.sub('[^A-Za-z0-9-]+', '', data)
            return data
        except Exception as e:
            print('clean seo error: '+ str(e))

    def saveSql(self, df, tableName):
        try:
            df.to_sql(tableName,self.engine, if_exists="replace", method=None, chunksize=20)
        except:
            print('savesql error: '+ str(e))
       