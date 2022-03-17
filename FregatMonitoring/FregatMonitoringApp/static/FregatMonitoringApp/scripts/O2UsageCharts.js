function RenderChart_o2(chart_data){
  am5.ready(function() {
    if(am5.registry.rootElements.length > 0){ //Если контейнер am5 уже инициализирован(при обновлении)
      for(i=0; i<am5.registry.rootElements.length; i++){
        if (am5.registry.rootElements[i].dom.id == "o2-usage-chartdiv"){
          var root = am5.registry.rootElements[i];
          i = am5.registry.rootElements.length //выходим из цикла
        } else if(i==am5.registry.rootElements.length-1){//Не нашли
          var root = am5.Root.new("o2-usage-chartdiv");
        }
      }
    } else {//Если контейнер am5 ещё не инициализирован(при первичной загрузке)
      var root = am5.Root.new("o2-usage-chartdiv");
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

    var o2_summary=0;  //кислород за весь период всего
    var o2_p1_sum = 0; //кислород за весь период на 1 печи
    var o2_p2_sum = 0; //кислород за весь период на 2 печи
    var o2_f_sum = 0; //кислород за весь период на фурме
    for (let i=0; i<chart_data[0][1].length; i++){
      o2_p1_sum=o2_p1_sum+chart_data[1][1][i].value //furnace_1_o2
      o2_p2_sum=o2_p2_sum+chart_data[3][1][i].value //furnace_2_o2
      o2_f_sum=o2_f_sum+chart_data[4][1][i].value //furma_o2
    }
    o2_summary = o2_p1_sum + o2_p2_sum + o2_f_sum

    document.getElementById("O2_consumpt_sum").innerHTML = o2_summary.toFixed(1)

    // Set data
    // https://www.amcharts.com/docs/v5/charts/percent-charts/pie-chart/#Setting_data
    series.data.setAll([{
      category: "Печь №2",
      value: o2_p2_sum
    }, {
      category: "Печь №1",
      value: o2_p1_sum
    },{
      category: "Фурма",
      value: o2_f_sum
    }]);

    series.appear(1500, 100);

  }); // end am5.ready()
}  