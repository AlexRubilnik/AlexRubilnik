#!/usr/bin/env python3

from typing import Any
import pyodbc
import cgi

driver='DRIVER={SQL Server}'
server='SERVER=FRGV202X\PRODUCTION'
port='PORT=1433'
db='DATABASE=FX_Hist'
user = 'UID=operator'
pw = 'PWD=fregat'
conn_str = ';'.join([driver, server, port, db, user, pw])
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

input_data = cgi.FieldStorage()

def getAutoMeltsInfo(DeltaT,furnace_no):
    return cursor.execute("UPDATE FX_Hist.dbo.AutoMelts SET DeltaT="+str(DeltaT)+"where Furnace_No="+str(furnace_no)).fetchone()

if input_data['ChangeDeltaT1_btn'].value != Any:
    row = getAutoMeltsInfo(input_data['ChangeDeltaT1_btn'].value, 1)
    print(1)

if input_data['ChangeDeltaT2_btn'].value != Any:
    row = getAutoMeltsInfo(input_data['ChangeDeltaT1_btn'].value, 2)  
    print(2)  



