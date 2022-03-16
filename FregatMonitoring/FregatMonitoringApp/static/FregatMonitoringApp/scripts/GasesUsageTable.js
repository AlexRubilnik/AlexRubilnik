//Функции для работы с удалением и добавением обработчиков событий нажатия кнопок
var _eventHandlers = {}; // somewhere global

const addListener = (node, event, handler, capture = false) => {
  if (!(event in _eventHandlers)) {
    _eventHandlers[event] = []
  }
  // here we track the events and their nodes (note that we cannot
  // use node as Object keys, as they'd get coerced into a string
  _eventHandlers[event].push({ node: node, handler: handler, capture: capture })
  node.addEventListener(event, handler, capture)
}

const removeAllListeners = (targetNode, event) => {
  // remove listeners from the matching nodes
  _eventHandlers[event]
    .filter(({ node }) => node === targetNode)
    .forEach(({ node, handler, capture }) => node.removeEventListener(event, handler, capture))

  // update _eventHandlers global
  _eventHandlers[event] = _eventHandlers[event].filter(
    ({ node }) => node !== targetNode,
  )
}

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
    //Удаляем обработчики с кнопок импорта в csv и xlsx, если опреелены
    try {
        removeAllListeners(document.getElementById("download-csv"), 'click')
        removeAllListeners(document.getElementById("download-xlsx"), 'click')
    } catch{}

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
    addListener(document.getElementById("download-csv"),
                'click', 
                function(){
                    table.download("csv", "data.csv");
                }, 
                false);

    //trigger download of data.xlsx file
    addListener(document.getElementById("download-xlsx"),
                'click', 
                function(){
                    table.download("xlsx", "data.xlsx", {sheetName:"Расходы газов"});
                }, 
                false);
} //RenderTable