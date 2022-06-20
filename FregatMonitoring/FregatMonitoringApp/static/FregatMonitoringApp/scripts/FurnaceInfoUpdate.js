cur_queue = 0;
var updSignals = document.getElementsByClassName("UpdSign")
var updSignals_1 = document.getElementsByClassName("UpdSign_1")

function FindSignals(){ 
        i = cur_queue
        
        var XHR = new XMLHttpRequest()
        if(updSignals[i].id !== ""){
            XHR.open('GET', '/FregatMonitoringApp/Furnace_info_s/'+updSignals[i].id+'/', true);
            XHR.timeout = 2000;
            XHR.send();
        } else {
          cur_queue=cur_queue+1; 
          if (cur_queue >= updSignals.length){
            cur_queue=0;
          } 
        }

        XHR.onreadystatechange = function() {
            if (this.readyState == 4) {
              cur_queue=cur_queue+1; //запрос завершён
              if (cur_queue >= updSignals.length){
                cur_queue=0;
              } 
            }           
            if (this.readyState != 4) return;

            if (this.status != 200) {
               // обработать ошибку
               //alert('ошибка: ' + (this.status ? this.statusText : 'запрос не удался') );
               return;
            }
              
            text = JSON.parse(this.responseText);
            for(j=0; j<text.length; j++){
              if(text[j].tagindex){ 
                var tab = document.getElementById(text[j].tagindex);
              }

              if(tab!=null){
                if (text[j].tagindex == 57 || text[j].tagindex == 78  || text[j].tagindex == 80  || text[j].tagindex == 79){ //дежурный режим or основной режим на 1 и 2 печи
                  tab = document.getElementById(text[j].tagindex);
                  if ( text[j].val == 1){
                    tab.className = "UpdSign red-lamp"
                  } else {
                    tab.className = "UpdSign black-lamp"
                  }
                } else {
                  tab.innerHTML = text[j].val;
                }
            }  
        };
        delete(XHR);  
      }     
}

setInterval(FindSignals,300);   

function AutoMeltInfoUpdate(){ 
  var XHR = new XMLHttpRequest()
  fur_no = document.getElementById("FurnaceNo");
  if(fur_no){
      if (fur_no.innerHTML=="Печь №1. Основные параметры"){
        XHR.open('GET', '/FregatMonitoringApp/Furnace_info_a/1/', true);
      } else {
        XHR.open('GET', '/FregatMonitoringApp/Furnace_info_a/2/', true);
      }  
      XHR.timeout = 2000;
      XHR.send();
  } 

  XHR.onreadystatechange = function() {
      if (this.readyState == 4) {
        cur_queue=cur_queue+1; //запрос завершён
        if (cur_queue >= updSignals.length){
          cur_queue=0;
        } 
      }           
      if (this.readyState != 4) return;

      if (this.status != 200) return;
        
      data = JSON.parse(this.responseText);
      for (text in data){
        var tab = document.getElementById(text);
        if(tab!=null){
            tab.innerHTML = data[text];
        }
      }  
        
  };
  delete(XHR);  
     
}

function color_power_sp_if_reduce(cur_power_tag_index, power_sp_tag_index){
  power_cur = document.getElementById(cur_power_tag_index);
  power_sp = document.getElementById(power_sp_tag_index);
  
  if(power_cur != null && power_sp != null)
      if (Number(power_sp.innerHTML)-Number(power_cur.innerHTML) == 0){
          power_cur.style.color = "green";
      } else if (Number(power_sp.innerHTML)-Number(power_cur.innerHTML) > 0 && Number(power_sp.innerHTML)-Number(power_cur.innerHTML) <= 200){
          power_cur.style.color = "orange";
      } else if (Number(power_sp.innerHTML)-Number(power_cur.innerHTML)> 200) {
          power_cur.style.color = "red";
      }  else {
          power_cur.style.color = "red";
      }
}

setInterval(AutoMeltInfoUpdate,3000); 

//Обновляем цвет значения текущей мощности. Если мощность ниже заданной - постепенно краснеет
setInterval(()=>color_power_sp_if_reduce("60", "power_sp_base"),1000); //для первой печи
setInterval(()=>color_power_sp_if_reduce("61", "power_sp_base"),1000); //для второй печи