function ChangeDeltaT(input){
    var XHR = new XMLHttpRequest();

    if(input.name == 'ChangeDeltaT1_btn'){
        var DeltaT_stp = document.getElementById('DeltaT1_stp');
        if(DeltaT_stp.value!=NaN){
            XHR.open('GET', 'cgi-bin/ChangeDeltaMethod.py?update=1&'+input.name+'='+DeltaT_stp.value, true);
            XHR.send();
        }
    }
    else if( input.name == 'ChangeDeltaT2_btn'){
        var DeltaT_stp = document.getElementById('DeltaT2_stp');
        if(DeltaT_stp.value!=NaN){
            XHR.open('GET', 'cgi-bin/ChangeDeltaMethod.py?update=1&'+input.name+'='+DeltaT_stp.value, true);
            XHR.send();
        }
        
    }
    XHR.onreadystatechange = function() {
        if (this.readyState != 4) return;

        if (this.status != 200) {
           // обработать ошибку
           alert('ошибка: ' + (this.status ? this.statusText : 'запрос не удался') );
           return;
        }

    };
    delete(XHR);
}