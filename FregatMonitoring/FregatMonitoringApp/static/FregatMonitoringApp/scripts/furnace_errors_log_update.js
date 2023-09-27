var marker_run = false;

function furnace_errors_log_update(furnace_no){ 
  start_time = document.getElementById('start_time').value
  stop_time = document.getElementById('stop_time').value

  data_download_marker_on_off(false); //Показываем маркер "Подождите. Идёт загрузка данных..."
  marker_run=true; //Запускаем бегущий маркер
  charts_tables_on_off(true); //Убираем таблицы и графики
 
  var XHR = new XMLHttpRequest()
      request_str = "/FregatMonitoringApp/FurnaceErrorsLogData/"+furnace_no+"/";
      let q_flag = false;
      if (furnace_no == "1" || furnace_no == "2"){
        request_str = request_str + '?furnace_no='+furnace_no
        q_flag = true;
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
      document.getElementById("furnace_errors_log_block").style['opacity'] = hidden_t
  } catch {}
}

//Build Tabulator
function RenderLog(TableData){

  let table_data = []
  for (let i = 0; i < TableData.length; i++){   
      let row = { 
        timestamp : TableData[i].timestamp,
        error : TableData[i].error,
        ng_press : TableData[i].ng_press,
        o2_press : TableData[i].o2_press,
        ng_flow : TableData[i].ng_flow,
        o2_flow : TableData[i].o2_flow,
        air_flow : TableData[i].air_flow,
      }       
      table_data.push(row)

  }

  var table = new Tabulator("#furnace_errors_log_table", {
  placeholder:"Нет данных",
  data: table_data,
  columns:[
      {//create column group
          title:"Журнал",
          columns:[
              {title:"Время", field:"timestamp", hozAlign:"center", width:180},
              {title:"Ошибка", field:"error", hozAlign:"left", width:700},
              {title:"Р_ПГ", field:"ng_press", hozAlign:"center", width:120},
              {title:"Р_О2", field:"o2_press", hozAlign:"center", width:140},
              {title:"Q_ПГ", field:"ng_flow", hozAlign:"center", width:140},
              {title:"Q_O2", field:"o2_flow", hozAlign:"center", width:130},
              {title:"Q_воздуха", field:"air_flow", hozAlign:"center", width:200},
          ],
      },
  ],
  });

} //RenderTable