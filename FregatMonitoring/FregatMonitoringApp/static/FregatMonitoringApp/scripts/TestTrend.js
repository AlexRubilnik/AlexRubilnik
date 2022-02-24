
function FurnaceBaseTrendsDataUpdate(){ 
  furnace_no = document.getElementById('Furnace_No').innerText
  start_time = document.getElementById('start_time').value
  stop_time = document.getElementById('stop_time').value
  if(am5.registry.rootElements[0] != null){
    var root = am5.registry.rootElements[0]
    root.dispose();
  }
    
  var XHR = new XMLHttpRequest()
      XHR.open('GET', '/FregatMonitoringApp/FurnaceBaseTrendsData/'+furnace_no+'/?start='+start_time+'&stop='+stop_time, true);
      //XHR.timeout = 2000;
      XHR.send();

  XHR.onreadystatechange = function() {
      if (this.readyState == 4) {
             //запрос завершён
      }           
      if (this.readyState != 4) return;

      if (this.status != 200) return;
        
      data = JSON.parse(this.responseText); 
      RenderTrends(data)       
  };
  delete(XHR);  
     
}


function RenderTrends(series_data){
  // Create root element
  // https://www.amcharts.com/docs/v5/getting-started/#Root_element 
  if(am5.registry.rootElements[0] != null){
    var root = am5.registry.rootElements[0] 
  } else {      
    var root = am5.Root.new("chartdiv");
  }  
  
  // Set themes
  // https://www.amcharts.com/docs/v5/concepts/themes/ 
  root.setThemes([
    am5themes_Animated.new(root),
    am5themes_Kelly.new(root)
  ]);           
  
  // Create chart
  // https://www.amcharts.com/docs/v5/charts/xy-chart/
  var chart = root.container.children.push(am5xy.XYChart.new(root, {
    panX: true,
    panY: true,
    wheelX: "panX",
    wheelY: "zoomX",
    maxTooltipDistance: 0
  }));

  // Create axes
  // https://www.amcharts.com/docs/v5/charts/xy-chart/axes/
  var xAxis = chart.xAxes.push(am5xy.DateAxis.new(root, {
    maxDeviation: 0.2,
    baseInterval: {
      timeUnit: "minute",
      count: 1
    },
    renderer: am5xy.AxisRendererX.new(root, {}),
    tooltip: am5.Tooltip.new(root, {})
  }));
  
  var yAxis = chart.yAxes.push(am5xy.ValueAxis.new(root, {
    renderer: am5xy.AxisRendererY.new(root, {})
  }));
  
  
  // Add series
  // https://www.amcharts.com/docs/v5/charts/xy-chart/series/
  for (var i = 0; i < series_data.length; i++) {
    var series = chart.series.push(am5xy.LineSeries.new(root, {
      name: series_data[i][0][0],
      xAxis: xAxis,
      yAxis: yAxis,
      valueYField: "value",
      valueXField: "date",
      legendValueText: "{valueY}",
      tooltip: am5.Tooltip.new(root, {
        pointerOrientation: "horizontal",
        labelText: "[bold]{name}[/]\n{categoryX}: {valueY}"
      })
    }));
        
    //var data = generateDatas(100);
    //series.data.setAll(data);
    series.data.setAll(series_data[i][1]);
  
    // Make stuff animate on load
    // https://www.amcharts.com/docs/v5/concepts/animations/
    series.appear();
  }
  
  // Add cursor
  // https://www.amcharts.com/docs/v5/charts/xy-chart/cursor/
  var cursor = chart.set("cursor", am5xy.XYCursor.new(root, {
    behavior: "none"
  }));
  cursor.lineY.set("visible", false);
  
  // Add scrollbar
  // https://www.amcharts.com/docs/v5/charts/xy-chart/scrollbars/
  chart.set("scrollbarX", am5.Scrollbar.new(root, {
    orientation: "horizontal"
  }));
  
  chart.set("scrollbarY", am5.Scrollbar.new(root, {
    orientation: "vertical"
  }));
  
  
  // Add legend
  // https://www.amcharts.com/docs/v5/charts/xy-chart/legend-xy-series/
  var legend = chart.rightAxesContainer.children.push(am5.Legend.new(root, {
    width: 250,
    paddingLeft: 15,
    height: am5.percent(120)
  }));
  
  // When legend item container is hovered, dim all the series except the hovered one
  legend.itemContainers.template.events.on("pointerover", function(e) {
    var itemContainer = e.target;
  
    // As series list is data of a legend, dataContext is series
    var series = itemContainer.dataItem.dataContext;
  
    chart.series.each(function(chartSeries) {
      if (chartSeries != series) {
        chartSeries.strokes.template.setAll({
          strokeOpacity: 0.15,
          stroke: am5.color(0x000000)
        });
      } else {
        chartSeries.strokes.template.setAll({
          strokeWidth: 3
        });
      }
    })
  })
  
  // When legend item container is unhovered, make all series as they are
  legend.itemContainers.template.events.on("pointerout", function(e) {
    var itemContainer = e.target;
    var series = itemContainer.dataItem.dataContext;
  
    chart.series.each(function(chartSeries) {
      chartSeries.strokes.template.setAll({
        strokeOpacity: 1,
        strokeWidth: 1,
        stroke: chartSeries.get("fill")
      });
    });
  })
  
  legend.itemContainers.template.set("width", am5.p100);
  legend.valueLabels.template.setAll({
    //width: am5.p100,
    textAlign: "right",
    fontSize: 15,
    fontWeight: "400"
  });
  legend.labels.template.setAll({
    width: am5.p100,
    fontSize: 15,
    fontWeight: "400"
  });
  
  // It's is important to set legend data after all the events are set on template, otherwise events won't be copied
  legend.data.setAll(chart.series.values);
  
  
  // Make stuff animate on load
  // https://www.amcharts.com/docs/v5/concepts/animations/
  chart.appear(1000, 100);
            
  var exporting = am5plugins_exporting.Exporting.new(root, {
    menu: am5plugins_exporting.ExportingMenu.new(root, {}),
    jpgOptions: {
      quality: 1,
      maintainPixelRatio: true
    },
    dataSource: data  
  });
            
}

am5.ready(function() {

  FurnaceBaseTrendsDataUpdate();
 
}); // end am5.ready()