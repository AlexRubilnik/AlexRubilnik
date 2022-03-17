function RenderChart_gas(chart_data){
  am5.ready(function() {
    if(am5.registry.rootElements.length > 0){ //Если контейнер am5 уже инициализирован(при обновлении)
      for(i=0; i<am5.registry.rootElements.length; i++){
        if (am5.registry.rootElements[i].dom.id == "gas-usage-chartdiv"){
          var root = am5.registry.rootElements[i];
          i = am5.registry.rootElements.length //выходим из цикла
        } else if(i==am5.registry.rootElements.length-1){//Не нашли
          var root = am5.Root.new("gas-usage-chartdiv");
        }
      }
    } else {//Если контейнер am5 ещё не инициализирован(при первичной загрузке)
      var root = am5.Root.new("gas-usage-chartdiv");
    }  

    root.container.children.clear();
      
    // Set themes
    // https://www.amcharts.com/docs/v5/concepts/themes/
    root.setThemes([
      am5themes_Animated.new(root)
    ]);

    // Create chart
    // https://www.amcharts.com/docs/v5/charts/percent-charts/pie-chart/
    var chart = root.container.children.push(
      am5percent.PieChart.new(root, {
        endAngle: 270
      })
    );

    // Create series
    // https://www.amcharts.com/docs/v5/charts/percent-charts/pie-chart/#Series
    var series = chart.series.push(
      am5percent.PieSeries.new(root, {
        valueField: "value",
        categoryField: "category",
        endAngle: 270
      })
    );

    series.states.create("hidden", {
      endAngle: -90
    });

    var data = []
    var gas_summary=0;  //газ за весь период всего
    var gas_p1_sum = 0; //газ за весь период на 1 печи
    var gas_p2_sum = 0; //газ за весь период на 2 печи

    for (let i=0; i<chart_data[0][1].length; i++){
      gas_p1_sum=gas_p1_sum+chart_data[0][1][i].value //furnace_1_gas
      gas_p2_sum=gas_p2_sum+chart_data[2][1][i].value //furnace_2_gas
    }
    gas_summary = gas_p1_sum + gas_p2_sum

    document.getElementById("PG_consumpt_sum").innerHTML = gas_summary.toFixed(1)

    // Set data
    // https://www.amcharts.com/docs/v5/charts/percent-charts/pie-chart/#Setting_data
    series.data.setAll([ {
      category: "Печь №2",
      value: gas_p2_sum
    }, {
      category: "Печь №1",
      value: gas_p1_sum
    }]);

    series.appear(1500, 100);

  }); // end am5.ready()
}  