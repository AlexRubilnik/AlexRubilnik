function GasesUsageDataUpdate(){ 
    report_type = document.getElementById('report_type').innerHTML 
    start_time = document.getElementById('start_time').value
    stop_time = document.getElementById('stop_time').value
      
    var XHR = new XMLHttpRequest()
        if (report_type == 'gases_usage_daily'){
            XHR.open('GET', '/FregatMonitoringApp/getGasesUsageData_daily/'+'?start='+start_time+'&stop='+stop_time, true);
        } else if (report_type == 'gases_usage_per_day'){
            XHR.open('GET', '/FregatMonitoringApp/getGasesUsageData_hourly/'+'?start='+start_time+'&stop='+stop_time, true);
        }
        //XHR.timeout = 2000;
        XHR.send();
  
    XHR.onreadystatechange = function() {
        if (this.readyState == 4) {
               //запрос завершён
        }           
        if (this.readyState != 4) return;
  
        if (this.status != 200) return;
        if (this.status = 200){
            t_data = JSON.parse(this.responseText); 
            RenderTable(t_data);
            RenderChart_1(t_data);
        }       
    };
    delete(XHR);  
       
}

GasesUsageDataUpdate();

//Build Tabulator
function RenderTable(TableData){
        //autotest to check if data series order is correct 
        if(TableData[0][0] != 'furnace_1_Gas' || TableData[1][0] != 'furnace_1_O2' || 
           TableData[2][0] != 'furnace_2_Gas' || TableData[3][0] != 'furnace_2_O2'  || TableData[4][0] != 'furma'){
            alert('Внимание! Данные в отчёте не корректные. Нарушен порядок передачи данных. Обратитесь к разработчику')
        }

        let table_data = []
        for (let i = 0; i < TableData[0][1].length; i++){   
            let row = {data : TableData[0][1][i].date,
                       furnace1_gas: TableData[0][1][i].value,
                       furnace1_o2: TableData[1][1][i].value,
                       furnace2_gas: TableData[2][1][i].value,
                       furnace2_o2: TableData[3][1][i].value,
                       furma: TableData[4][1][i].value

            }       
            table_data.push(row)
        }

        var table = new Tabulator("#gases-usage-table", {
        height:"550px",
        placeholder:"Нет данных",
        data: table_data,
        columns:[
            {//create column group
                title:"",
                columns:[
                {title:"Дата", field:"data", hozAlign:"right", sorter:"number", width:150},
                ],
            },
            {//create column group
                title:"Печь №1",
                columns:[
                {title:"Газ, [м3]", field:"furnace1_gas", hozAlign:"right", sorter:"number", width:100},
                {title:"О2, [м3]", field:"furnace1_o2", hozAlign:"center", width:100},
                ],
            },
            {//create column group
                title:"Печь №2",
                columns:[
                    {title:"Газ, [м3]", field:"furnace2_gas", hozAlign:"right", sorter:"number", width:100},
                    {title:"О2, [м3]", field:"furnace2_o2", hozAlign:"center", width:100},
                ],
            },
            {//create Column group
                title:"Фурма",
                columns:[
                    {title:"О2, [м3]", field:"furma", hozAlign:"center", width:100},
                ],
            },
            ],
        });


    //trigger download of data.csv file
    document.getElementById("download-csv").addEventListener("click", function(){
        table.download("csv", "data.csv");
    });

    //trigger download of data.xlsx file
    document.getElementById("download-xlsx").addEventListener("click", function(){
        table.download("xlsx", "data.xlsx", {sheetName:"My Data"});
    });

} //RenderTable