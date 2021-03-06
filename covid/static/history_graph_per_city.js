am4core.ready(function() {

// Themes begin
am4core.useTheme(am4themes_animated);
// Themes end




// Create chart instance
var chart = am4core.create("history_graph_per_city", am4charts.XYChart);

// Create axes
var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());

var cities = ['Paphos','Limassol','Nicosia','Larnaca'];
for (var i = 0; i < cities.length; i++) {
  createSeries("value", cities[i],all_data.daily_count_per_city[cities[i]]);
}

// Create series
function createSeries(s, name,data) {
  var series = chart.series.push(new am4charts.LineSeries());
  series.dataFields.valueY = "value";
  series.dataFields.dateX = "date";
  series.name = name;

  var segment = series.segments.template;
  segment.interactionsEnabled = true;

  var hoverState = segment.states.create("hover");
  hoverState.properties.strokeWidth = 3;

  var dimmed = segment.states.create("dimmed");
  dimmed.properties.stroke = am4core.color("#dadada");

  segment.events.on("over", function(event) {
    processOver(event.target.parent.parent.parent);
  });

  segment.events.on("out", function(event) {
    processOut(event.target.parent.parent.parent);
  });
  for(var i=0;i<data.length;i++){
    data[i].date = new Date(data[i].date);
  }
  // var data = [];
  // var value = Math.round(Math.random() * 100) + 100;
  // for (var i = 1; i < 100; i++) {
  //   value += Math.round((Math.random() < 0.5 ? 1 : -1) * Math.random() * 30 + i / 5);
  //   var dataItem = { date: new Date(2018, 0, i) };
  //   dataItem["value" + s] = value;
  //   data.push(dataItem);
  // }

  series.data = data;
  return series;
}

chart.legend = new am4charts.Legend();
chart.legend.position = "right";
chart.legend.scrollable = true;
chart.legend.itemContainers.template.events.on("over", function(event) {
  processOver(event.target.dataItem.dataContext);
})

chart.legend.itemContainers.template.events.on("out", function(event) {
  processOut(event.target.dataItem.dataContext);
})

function processOver(hoveredSeries) {
  hoveredSeries.toFront();

  hoveredSeries.segments.each(function(segment) {
    segment.setState("hover");
  })

  chart.series.each(function(series) {
    if (series != hoveredSeries) {
      series.segments.each(function(segment) {
        segment.setState("dimmed");
      })
      series.bulletsContainer.setState("dimmed");
    }
  });
}

function processOut(hoveredSeries) {
  chart.series.each(function(series) {
    series.segments.each(function(segment) {
      segment.setState("default");
    })
    series.bulletsContainer.setState("default");
  });
}

}); // end am4core.ready()
