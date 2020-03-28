$(document).ready(function () {
  am4core.ready(function() {

  // Themes begin
  am4core.useTheme(am4themes_animated);
  // Themes end

  var chart = am4core.create("chartdiv", am4charts.XYChart);

  var data = [];
  for(var i=0;i<all_data.count_per_hour.length;i++){
    data.push({'date':new Date(all_data.count_per_hour[i].datetime),'value':all_data.count_per_hour[i].value});
  }
  console.log(data);
  load_graph();

  function load_graph(){
    chart.data = data;

    // Create axes
    var xAxis = new am4charts.DateAxis();
    xAxis.baseInterval = {
      timeUnit: "hour",
      count: 1
    };
    var dateAxis = chart.xAxes.push(xAxis);
    dateAxis.renderer.minGridDistance = 60;

    var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());

    // Create series
    var series = chart.series.push(new am4charts.LineSeries());
    series.dataFields.valueY = "value";
    series.dataFields.dateX = "date";
    series.tooltipText = "{value}"

    series.tooltip.pointerOrientation = "vertical";

    chart.cursor = new am4charts.XYCursor();
    chart.cursor.snapToSeries = series;
    chart.cursor.xAxis = dateAxis;

    //chart.scrollbarY = new am4core.Scrollbar();
    chart.scrollbarX = new am4core.Scrollbar();
  }


  }); // end am4core.ready()

});
