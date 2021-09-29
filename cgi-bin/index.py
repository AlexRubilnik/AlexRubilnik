#!/usr/bin/env python
# The line above ^ is important. Don't leave it out. It should be at the
# top of the file.

import cgi, cgitb # Not used, but will be needed later.

print("""
<!DOCTYPE html>
<html>
<head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
      <link rel="stylesheet" type="text/css" href="http://frgv006a:8000/css/style.css">
      <script src=http://frgv006a:8000/scripts/DataUpdate.js></script>
      <script src=http://frgv006a:8000/scripts/ChangeDeltaMethod.js></script>
</head>
<body>

<div class="header-bgd"> <!-- Header-->
       <table width="100%">
       <tr style="height:20px">
          <td class="header-brand">ООО "Фрегат"</td>
          <td class="orange-text cursive">Cloud monitoring service</td>  
          <td class="white-text">Сервис дистанционного мониторинга и управления</td>
          <td>
            <table width="100%"> 
            <tr>
               <td><table>
                 <tr>
                   <td class="white-text"> Пользователь: </td>

                   <td class="white-text"> Оператор      </td>
                 </tr>
                    </table>
               </td>
            </tr>  
            <td>
               <td><table> 
                  <tr class="white-text">
                    Оператор
                  </tr>    
                   </table> 
               </td>
            </tr>
            </table>
          </td>
       </tr>
       </table>
</div>
<div class="main_container">  <!-- Содержимое полностью-->
  <aside class="left-side-bar">
    <ul>
      <li>Печь №1</li>
      <li>Печь №2</li>
      <li>Линия розлива</li>
      <li>Рафинирование</li>
      <li>Тренды</li>
      <li>Отчёты</li>
    </ul>
  </aside>
  <div class="current_scr_container">
    <input id='curScr' type='hidden' value='monitor_scr'> 
    <table>
      <tr>
        <form id="ChangeDeltaT1Form"> 
        <td>Уставка дельта Т печь №1</td>
        <td><input id="DeltaT1_stp" value></td>
        <td><input class="btn" name="ChangeDeltaT1_btn" value="Изменить" onclick="ChangeDeltaT(this);"></td>
        </form>
      </tr>
      <tr>
        <form id="ChangeDeltaT2Form">
        <td>Уставка дельта Т печь №2</td>
        <td><input id="DeltaT2_stp" value></td>
        <td><input class="btn" name="ChangeDeltaT2_btn" value="Изменить" onclick="ChangeDeltaT(this);"></td>
        </form>
      </tr>
    </table>
  </div>
</div>

</body>
</html>""")