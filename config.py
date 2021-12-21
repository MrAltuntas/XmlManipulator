URL = 'https://kayderoutdoor.sentos.com.tr/xml-out/3_deneme'
OUTERFIELDS = ["Urunler","Urun"]
#change fields with separators split 
FIELDNAMES = ["kategori_ismi"]
SEPARATORS = [">"]
INDIES = ["last"] # Options firstAndLast, first, last. Default first.

TIME = 60 #in second
SAVEASTXT = True
SAVEASSQL = True
ROWTOSTR = True

TABLENAME = 'kayzertest'
CONNECTIONSTRING=f'mssql+pyodbc://@MUSTAFA/kayzertest?driver=ODBC+Driver+13+for+SQL+Server'