//Build Tabulator
var table = new Tabulator("#example-table", {
    height:"400px",
    columns:[
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
                {title:"Газ, [м3]", field:"furnace1_gas", hozAlign:"right", sorter:"number", width:100},
                {title:"О2, [м3]", field:"furnace1_o2", hozAlign:"center", width:100},
            ],
        },
        {//create Column group
            title:"Фурма",
            columns:[
                {title:"О2, [м3]", field:"furnace1_o2", hozAlign:"center", width:100},
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
