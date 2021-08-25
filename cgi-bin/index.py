#!/usr/bin/env python3

Html='''<!DOCTYPE HTML>
<html>
<head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
      <link rel="stylesheet" type="text/css" href="style.css">
</head>
<body>

<div style="height:60px; margin-left:-15px; padding-bottom:0px; padding-top:0px; margin-right:-15px; margin-top:-15px; margin-bottom:-15px; background-color:rgb(22, 20, 20); opacity:0.8; box-shadow:  0 0 20px rgba(0,0,0,0.8);">
       <table border="0" width="100%" style="height:60px; padding-bottom:0px; padding-top:0px; border-collapse:collapse;">
       <tr style="height:20px">
          <td width="25%" align="right" style="font-size:40px; color:rgb(255, 127, 0); font-weight: 900; font-family: "Lato","Helvetica Neue",Helvetica,Arial,sans-serif;"  class="header-brand"> ООО Фрегат </td>
          <td width="10%" align="left" valign="top" style="color: #FF8C00; font-size: 16px; font-style:italic; padding-left: 10px; padding-top: 10px;">Cloud monitoring service</td>  
          <td width="45%" align="left" style="padding-left:90px; padding-top: 20px; font-size: 14px; color:white;">Сервис дистанционного мониторинга и управления</td>
          <td width="20%">
            <table  border="0" align="right" width="100%" style=" height:40px; padding:0%; margin-top:0px; border-collapse: collapse; border-color:white;"> 
            <tr style="border-color:white;">
               <td style="border-color:white;">
                 <table border="0">
                 <tr>
                   <td style="color:white;">Пользователь: </td>
                   <td style="color:white;">
                   </td>
                 </tr>      
                 </table>
               </td>
            </tr>  
            <tr style="border-color:white;">
               <td style="padding-bottom:0px; padding-top:0px;">
                  <table style="padding:inherit;" border="0" align="left"> 
                  <tr style="padding:inherit;">
                    Оператор
                  </tr>    
                  </table> 
               </td>
            </tr>
            </table>
          </td>
       </tr>
       </table>
</div>'''

print(Html)
print()
print()
print()
import pyodbc
driver='DRIVER={SQL Server}'
server='SERVER=FRGS005X'
port='PORT=1433'
db='DATABASE=Zebra'
user = 'UID=Zebra'
pw = 'PWD=123456'
conn_str = ';'.join([driver, server, port, db, user, pw])
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()
cursor.execute('select top 10 * from Zebra.dbo.Production')
row=cursor.fetchone()
rest_of_rows = cursor.fetchall()


print("<h1>Привет, Фрегат!</h1>")
print("<h2>Привет, Фрегат!</h2>")
for i in range(1,9):
    print('<div>'+str(row[i])+'</div>')
