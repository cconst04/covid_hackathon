am4core.ready(function() {

// Themes begin
am4core.useTheme(am4themes_animated);
// Themes end

// Create chart instance
var chart = am4core.create("baseline_compare", am4charts.XYChart);
// Add data
var data = all_data.baseline_comparison;
for(var i=0;i<data.length;i++){
  data[i].date=new Date(data[i].date);
  data[i].previousDate=new Date(data[i].previousDate);
}
console.log(data);
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
series.dataFields.valueY = "value1";
series.dataFields.dateX = "date";
series.strokeWidth = 2;
series.minBulletDistance = 10;
series.tooltipText = "[bold]{date.formatDate()}:[/] {value1}\n[bold]Previous Dates Average:[/] {value2}";
series.tooltip.pointerOrientation = "vertical";

// Create series
var series2 = chart.series.push(new am4charts.LineSeries());
series2.dataFields.valueY = "value2";
series2.dataFields.dateX = "date";
series2.strokeWidth = 2;
series2.strokeDasharray = "3,4";
series2.stroke = series.stroke;

// Add cursor
chart.cursor = new am4charts.XYCursor();
chart.cursor.xAxis = dateAxis;

}); // end am4core.ready()
