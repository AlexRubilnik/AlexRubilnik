var marker_run = false;

function auto_melts_log_update(){ 
  furnace_no = document.getElementById('furnace_no').value
  melt_number = document.getElementById('melt_number').value
  start_time = document.getElementById('start_time').value
  stop_time = document.getElementById('stop_time').value

  data_download_marker_on_off(false); //Показываем маркер "Подождите. Идёт загрузка данных..."
  marker_run=true; //Запускаем бегущий маркер
  charts_tables_on_off(true); //Убираем таблицы и графики
 
  var XHR = new XMLHttpRequest()
      request_str = "/FregatMonitoringApp/auto_melts_log_data/";
      let q_flag = false;
      if (furnace_no == "1" || furnace_no == "2"){
        request_str = request_str + '?furnace_no='+furnace_no
        q_flag = true;
      }
      if (melt_number != ""){
        if (q_flag) {
          request_str = request_str + '&melt_number='+melt_number
        } else {
          q_flag = true;
          request_str = request_str + '?melt_number='+melt_number
        }
      }
      if (start_time != ""){
        if (q_flag) {
          request_str = request_str + '&start='+start_time;
        } else {
          q_flag = true;
          request_str = request_str + '?start='+start_time;
        }
      }
      if (stop_time != ""){
        if (q_flag) {
          request_str = request_str + '&stop='+stop_time;
        } else {
          q_flag = true;
          request_str = request_str + '?stop='+stop_time;
        }
      }
      XHR.open('GET', request_str, true);
      //XHR.timeout = 2000;
      XHR.send();

  XHR.onreadystatechange = function() {
      if (this.readyState == 4) {
             //запрос завершён
      }           
      if (this.readyState != 4) return;

      if (this.status != 200) {
        marker_run=false; //Останавливаем бегущий маркер
        data_download_marker_on_off(true); //Скрываем маркер "Подождите. Идёт загрузка данных..."
        alert('Произошла ошибка при загрузке данных!')
        return;
      }  
        
      data = JSON.parse(this.responseText); 
      marker_run=false; //Останавливаем бегущий маркер
      data_download_marker_on_off(true); //Скрываем маркер "Подождите. Идёт загрузка данных..."
      charts_tables_on_off(false); //Показываем таблицы и графики
      RenderLog(data)       
  };
  delete(XHR);  
     
}

function data_download_marker_on_off(hidden){
  //Скрываем маркер "Подождите. Идёт загрузка данных..."
  document.getElementById("data-download-marker").hidden = hidden
  document.getElementById("ddm1").hidden = hidden
  document.getElementById("ddm2").hidden = hidden
  document.getElementById("ddm3").hidden = hidden
}

setInterval(function data_download_marker_run(){
  //Бегущий маркер "Подождите. Идёт загрузка данных..."
  if(marker_run) {
      if(document.getElementById("ddm1").hidden==true){ //все точки скрыты
          document.getElementById("ddm1").hidden = false //показываем первую
      } else if(document.getElementById("ddm2").hidden==true) {
          document.getElementById("ddm2").hidden = false //показываем вторую
      } else if(document.getElementById("ddm3").hidden==true) {
          document.getElementById("ddm3").hidden = false //показываем третью
      } else { 
          document.getElementById("ddm1").hidden = true //скрываем все
          document.getElementById("ddm2").hidden = true //скрываем все
          document.getElementById("ddm3").hidden = true //скрываем все
      }
  }
}, 500);


function charts_tables_on_off(hidden){ //Прячет содержимое страницы при загрузке новых данных
  var hidden_t = "1"
  if (hidden) {hidden_t="0"}
  try{
      document.getElementById("automelts-log-block").style['opacity'] = hidden_t
  } catch {}
}

//Build Tabulator
function RenderLog(TableData){

  let table_data = []
  for (let i = 0; i < TableData.length; i++){   
      let row = { 
        furnace_no : TableData[i].furnace_no,
        melt_number : TableData[i].melt_number,
        melt_type : TableData[i].melt_type,
        current_step : TableData[i].current_step,
        current_substep : TableData[i].current_substep,
        auto_mode : TableData[i].auto_mode,
        date_time : TableData[i].date_time,
        power_sp : TableData[i].power_sp,
        rotation_sp : TableData[i].rotation_sp,
        alpha_sp : TableData[i].alpha_sp,
        sub_step_time : TableData[i].sub_step_time
      }       
      table_data.push(row)

  }

  var table = new Tabulator("#automelts-log-table", {
  placeholder:"Нет данных",
  data: table_data,
  columns:[
      {//create column group
          title:"Режим",
          columns:[
              {title:"Время", field:"date_time", hozAlign:"center", width:180},
              {title:"№ Печи", field:"furnace_no", hozAlign:"right", sorter:"number", width:100},
              {title:"№ Плавки", field:"melt_number", hozAlign:"center", width:120},
              {title:"Тип плавки", field:"melt_type", hozAlign:"center", width:140},
              {title:"Стадия", field:"current_step", hozAlign:"center", width:140},
              {title:"Шаг", field:"current_substep", hozAlign:"center", width:130},
              {title:"Режим", field:"auto_mode", hozAlign:"center", width:200},
          ],
      },
      {
          title:"Уставки",
          columns:[
              {title:"Мощность, кВт", field:"power_sp", hozAlign:"center", width:140},
              {title:"Вращение, [%]", field:"rotation_sp", hozAlign:"center", width:140},
              {title:"Обогащение, [%]", field:"alpha_sp", hozAlign:"center", width:150},
              {title:"Время шага, [мин]", field:"sub_step_time", hozAlign:"center", width:160},
          ],
      },
  ],
  });

} //RenderTable