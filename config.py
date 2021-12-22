URL = 'https://kayderoutdoor.sentos.com.tr/xml-out/3_deneme'
OUTERFIELDS = ["Urunler","Urun"]
#change fields with separators split 
FIELDNAMES = ["kategori_ismi"]
SEPARATORS = [">"]
INDIES = ["last"] # Options firstAndLast, first, last. Default first.

TIME = 60 #in second
SAVEASTXT = True
TXTNAME = "data.json"
ROWTOSTR = True
SAVEASSQL = True
TABLENAME = 'kayzertest'

CREATERELATEDTABLE = True
RELATEDFIELDNAME = ["Varyantlar"]
RELATEDOUTERFIELDS = [["Varyant"]]
RELATEDTABLENAME = ["Variants"]

CONNECTIONSTRING=f'mssql+pyodbc://@MUSTAFA/kayzertest?driver=ODBC+Driver+13+for+SQL+Server'