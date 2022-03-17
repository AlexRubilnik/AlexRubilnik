function RenderChart_1(chart_data){
  am5.ready(function() {
    if(am5.registry.rootElements.length > 0){ //Если контейнер am5 уже инициализирован(при обновлении)
      for(i=0; i<am5.registry.rootElements.length; i++){
        if (am5.registry.rootElements[i].dom.id == "gases-usage-chartdiv"){
          var root = am5.registry.rootElements[i];
          i = am5.registry.rootElements.length //выходим из цикла
        } else if(i==am5.registry.rootElements.length-1){//Не нашли
          var root = am5.Root.new("gases-usage-chartdiv");
        }
      }
    } else {//Если контейнер am5 ещё не инициализирован(при первичной загрузке)
      var root = am5.Root.new("gases-usage-chartdiv");
    }  

    root.container.children.clear();
      
  // Set themes
  // https://www.amcharts.com/docs/v5/concepts/themes/
  root.setThemes([
    am5themes_Animated.new(root),
  ]);


  // Create chart
  // https://www.amcharts.com/docs/v5/charts/xy-chart/
  var chart = root.container.children.push(am5xy.XYChart.new(root, {
    panX: false,
    panY: false,
    wheelX: "panX",
    wheelY: "zoomX",
    layout: root.verticalLayout
  }));


  // Add legend
  // https://www.amcharts.com/docs/v5/charts/xy-chart/legend-xy-series/
  var legend = chart.children.push(
    am5.Legend.new(root, {
      centerX: am5.p50,
      x: am5.p50
    })
  );

  var data = []
  for (let i=0; i<chart_data[0][1].length; i++){
    let point = {
      "date": chart_data[0][1][i].date,
      "gas": (chart_data[0][1][i].value+chart_data[2][1][i].value), //furnace_1_gas + furnace_2_gas
      "o2": (chart_data[1][1][i].value+chart_data[3][1][i].value+chart_data[4][1][i].value) //furnace_1_o2 + furnace_2_02 + furma_o2
    }
    data.push(point)
  }

  // Create axes
  // https://www.amcharts.com/docs/v5/charts/xy-chart/axes/
  var xAxis = chart.xAxes.push(am5xy.CategoryAxis.new(root, {
    categoryField: "date",
    renderer: am5xy.AxisRendererX.new(root, {
      cellStartLocation: 0.1,
      cellEndLocation: 0.9
    }),
    tooltip: am5.Tooltip.new(root, {})
  }));

  xAxis.data.setAll(data);

  var yAxis = chart.yAxes.push(am5xy.ValueAxis.new(root, {
    renderer: am5xy.AxisRendererY.new(root, {})
  }));


  // Add series
  // https://www.amcharts.com/docs/v5/charts/xy-chart/series/
  function makeSeries(name, fieldName, color) {
    var series = chart.series.push(am5xy.ColumnSeries.new(root, {
      name: name,
      xAxis: xAxis,
      yAxis: yAxis,
      valueYField: fieldName,
      categoryXField: "date",
      fill: am5.color(color),
      stroke: am5.color(color)
    }));

    series.columns.template.setAll({
      tooltipText: "[bold]{name}[/]\n{categoryX}: [bold]{valueY}",
      width: am5.percent(90),
      tooltipY: 0
    });

    series.data.setAll(data);

    // Make stuff animate on load
    // https://www.amcharts.com/docs/v5/concepts/animations/
    series.appear();

    series.bullets.push(function () {
      return am5.Bullet.new(root, {
        locationY: 0,
        sprite: am5.Label.new(root, {
          text: "{valueY}",
          fill: root.interfaceColors.get("alternativeText"),
          centerY: 0,
          centerX: am5.p50,
          populateText: true
        })
      });
    });

    legend.data.push(series);
  }

  makeSeries("Природный газ", "gas", 0xff7f00);
  makeSeries("Кислород", "o2", 0x4473b3 );

  // Make stuff animate on load
  // https://www.amcharts.com/docs/v5/concepts/animations/
  chart.appear(2000, 100);

  }); // end am5.ready()
}  