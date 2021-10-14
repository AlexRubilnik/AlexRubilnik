#!/usr/bin/env python3

import pyodbc
import json
import cgi

driver='DRIVER={SQL Server}'
server='SERVER=FRGV202X\PRODUCTION'
port='PORT=1433'
db='DATABASE=FX_Hist'
user = 'UID=ProdReader'
pw = 'PWD=123'
conn_str = ';'.join([driver, server, port, db, user, pw])
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

input_data = cgi.FieldStorage()

def getAutoMeltsInfo(furnace_no):
    return cursor.execute("select * from FX_Hist.dbo.AutoMelts where Furnace_No="+str(furnace_no)).fetchone()

if input_data['curscr'].value == 'monitor_scr':
    row1 = getAutoMeltsInfo(1)
    row2= getAutoMeltsInfo(2)
    response = {
    "DeltaT1_stp": row1[6],
    "DeltaT2_stp": row2[6],
    }  
print("Content-type: text/html\n")    
responseJson = json.dumps(response)
print(responseJson)

cursor.close()
conn.close()

