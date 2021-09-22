    function DownloadData(){
        var curScr = document.getElementById('curScr')
        var XHR = new XMLHttpRequest()
        if(curScr !== null){
            XHR.open('GET','cgi-bin/DataUpdate.py?curscr='+curScr.value, true);

            XHR.send();
        }

        XHR.onreadystatechange = function() {
            if (this.readyState != 4) return;

            if (this.status != 200) {
               // обработать ошибку
               //alert('ошибка: ' + (this.status ? this.statusText : 'запрос не удался') );
               return;
            }
              text = JSON.parse(this.responseText);

              var tab = document.getElementById('DeltaT1_stp');
              if(tab!=null){
                tab.value = text.DeltaT1_stp;
              }
              var tab = document.getElementById('DeltaT2_stp');
              if(tab!=null){
                tab.value = text.DeltaT2_stp;
              }

        };
        delete(XHR);   
    }

    setTimeout(DownloadData,1000);