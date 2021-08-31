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
    cursor.execute("UPDATE FX_Hist.dbo.AutoMelts SET DeltaT="+str(DeltaT)+"where Furnace_No="+str(furnace_no))
    conn.commit()
    return


if 'ChangeDeltaT1_btn' in input_data:
    if input_data['ChangeDeltaT1_btn'].value != None:
        row = getAutoMeltsInfo(input_data['ChangeDeltaT1_btn'].value, 1)

if 'ChangeDeltaT2_btn' in input_data:
    if input_data['ChangeDeltaT2_btn'].value != None:
        row = getAutoMeltsInfo(input_data['ChangeDeltaT2_btn'].value, 2)   

cursor.close()
conn.close()

