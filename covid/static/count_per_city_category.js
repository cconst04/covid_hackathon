// New map-pie series type that also allows lat/lon as center option.
// Also adds a sizeFormatter option to the series, to allow dynamic sizing
// of the pies.
Highcharts.seriesType('mappie', 'pie', {
  center: null, // Can't be array by default anymore
  clip: true, // For map navigation
  states: {
    hover: {
      halo: {
        size: 6
      }
    }
  },
  dataLabels: {
    enabled: false
  }
}, {
  getCenter: function () {
    var options = this.options,
      chart = this.chart,
      slicingRoom = 2 * (options.slicedOffset || 0);
    if (!options.center) {
      options.center = [null, null]; // Do the default here instead
    }
    // Handle lat/lon support
    if (options.center.lat !== undefined) {
      var point = chart.fromLatLonToPoint(options.center);
      options.center = [
        chart.xAxis[0].toPixels(point.x, true),
        chart.yAxis[0].toPixels(point.y, true)
      ];
    }
    // Handle dynamic size
    if (options.sizeFormatter) {
      options.size = options.sizeFormatter.call(this);
    }
    // Call parent function
    var result = Highcharts.seriesTypes.pie.prototype.getCenter.call(this);
    // Must correct for slicing room to get exact pixel pos
    result[0] -= slicingRoom;
    result[1] -= slicingRoom;
    return result;
  },
  translate: function (p) {
    this.options.center = this.userOptions.center;
    this.center = this.getCenter();
    return Highcharts.seriesTypes.pie.prototype.translate.call(this, p);
  }
});


var data = all_data.category_per_city,
  maxVotes = 0,
  reason1 = 'rgba(74,131,240,0.80)',
  reason2 = 'rgba(220,71,71,0.80)',
  reason3 = 'rgba(240,190,50,0.80)',
  reason4 = 'rgba(90,200,90,0.80)',
  reason5 = 'rgba(0,0,0,0.80)',
  reason6 = 'rgba(39,26,15,0.80)',
  reason7 = 'rgba(212,0,254,0.80)',
  reason8 = 'rgba(249,100,5,0.80)';



// Compute max votes to find relative sizes of bubbles
Highcharts.each(data, function (row) {
  maxVotes = Math.max(maxVotes, row[9]);
});

// Build the chart
var chart = Highcharts.mapChart('category_map', {
  title: {
    text: 'Cyprus Covid sms analysis'
  },

  chart: {
    animation: false // Disable animation, especially for zooming
  },

  colorAxis: {
    dataClasses: [{
      from: -1,
      to: 0,
      color: 'rgba(244,91,91,0.5)',
      name: 'Reason 1'
    }, {
      from: 0,
      to: 1,
      color: 'rgba(124,181,236,0.5)',
      name: 'Reason 2'
    }, {
      from: 2,
      to: 3,
      name: 'Reason 3',
      color: reason3
    }, {
      from: 3,
      to: 4,
      name: 'Reason 4',
      color: reason4
    }, {
      from: 4,
      to: 5,
      color: reason5,
      name: 'Reason 5'
    },
    {
      from: 5,
      to: 6,
      color: reason6,
      name: 'Reason 6'
    },
    {
      from: 6,
      to: 7,
      color: reason7,
      name: 'Reason 7'
    },
    {
      from: 7,
      to: 8,
      color: reason8,
      name: 'Reason 8'
    }]
  },

  mapNavigation: {
    enabled: true
  },
  // Limit zoom range
  yAxis: {
    minRange: 2300
  },

  tooltip: {
    useHTML: true
  },

  // Default options for the pies
  plotOptions: {
    mappie: {
      borderColor: 'rgba(255,255,255,0.4)',
      borderWidth: 1,
      tooltip: {
        headerFormat: ''
      }
    }
  },

  series: [{
    mapData: Highcharts.maps['countries/cy/cy-all'],
    data: data,
    name: 'States',
    borderColor: '#FFF',
    showInLegend: false,
    joinBy: ['name', 'id'],
    //demVotes keys: ['id', 'demVotes', 'repVotes', 'libVotes', 'grnVotes','sumVotes', 'value', 'pieOffset'],
    keys: ['id', 'reason1', 'reason2', 'reason3', 'reason4','reason5','reason6',
      'reason7','reason8','sumVotes', 'value', 'pieOffset'],
    tooltip: {
      headerFormat: '',
      pointFormatter: function () {
        var hoverVotes = this.hoverVotes; // Used by pie only
        return '<b>' + this.id + ' sms</b><br/>' +
          Highcharts.map([
            ['Reason 1', this.reason1, reason1],
            ['Reason 2', this.reason2, reason2],
            ['Reason 3', this.reason3, reason3],
            ['Reason 4', this.reason4, reason4],
            ['Reason 5', this.reason5, reason5],
            ['Reason 6', this.reason6, reason6],
            ['Reason 7', this.reason7, reason7],
            ['Reason 8', this.reason8, reason8]
          ].sort(function (a, b) {
            return b[1] - a[1]; // Sort tooltip by most votes
          }), function (line) {
            return '<span style="color:' + line[2] +
              // Colorized bullet
              '">\u25CF</span> ' +
              // Party and votes
              (line[0] === hoverVotes ? '<b>' : '') +
              line[0] + ': ' +
              Highcharts.numberFormat(line[1], 0) +
              (line[0] === hoverVotes ? '</b>' : '') +
              '<br/>';
          }).join('') +
          '<hr/>Total: ' + Highcharts.numberFormat(this.sumVotes, 0);
      }
    }
  }, {
    name: 'Separators',
    type: 'mapline',
    data: Highcharts.geojson(Highcharts.maps['countries/cy/cy-all'], 'mapline'),
    color: '#707070',
    showInLegend: false,
    enableMouseTracking: false
  }, {
    name: 'Connectors',
    type: 'mapline',
    color: 'rgba(130, 130, 130, 0.5)',
    zIndex: 5,
    showInLegend: false,
    enableMouseTracking: false
  }]
});

// When clicking legend items, also toggle connectors and pies
Highcharts.each(chart.legend.allItems, function (item) {
  var old = item.setVisible;
  item.setVisible = function () {
    var legendItem = this;
    old.call(legendItem);
    Highcharts.each(chart.series[0].points, function (point) {
      if (chart.colorAxis[0].dataClasses[point.dataClass].name === legendItem.name) {
        // Find this state's pie and set visibility
        Highcharts.find(chart.series, function (item) {
          return item.name === point.id;
        }).setVisible(legendItem.visible, false);
        // Do the same for the connector point if it exists
        var connector = Highcharts.find(chart.series[2].points, function (item) {
          return item.name === point.id;
        });
        if (connector) {
          connector.setVisible(legendItem.visible, false);
        }
      }
    });
    chart.redraw();
  };
});

// Add the pies after chart load, optionally with offset and connectors
Highcharts.each(chart.series[0].points, function (state) {
  if (!state.id) {
    return; // Skip points with no data, if any
  }

  var pieOffset = state.pieOffset || {},
    centerLat = parseFloat(state.properties.latitude),
    centerLon = parseFloat(state.properties.longitude);

  // Add the pie for this state
  chart.addSeries({
    type: 'mappie',
    name: state.id,
    zIndex: 8, // Keep pies above connector lines
    sizeFormatter: function () {
      var yAxis = this.chart.yAxis[0],
        zoomFactor = (yAxis.dataMax - yAxis.dataMin) /
          (yAxis.max - yAxis.min);
      return Math.max(
        this.chart.chartWidth / 45 * zoomFactor, // Min size
        this.chart.chartWidth / 11 * zoomFactor * state.sumVotes / maxVotes
      );
    },
    tooltip: {
      // Use the state tooltip for the pies as well
      pointFormatter: function () {
        return state.series.tooltipOptions.pointFormatter.call({
          id: state.id,
          hoverVotes: this.name,
          reason1: state.reason1,
          reason2: state.reason2,
          reason3: state.reason3,
          reason4: state.reason4,
          reason5: state.reason5,
          reason6: state.reason6,
          reason7: state.reason7,
          reason8: state.reason8,
          sumVotes: state.sumVotes
        });
      }
    },
    data: [{
      name: 'Reason 1',
      y: state.reason1,
      color: reason1
    }, {
      name: 'Reason 2',
      y: state.reason2,
      color: reason2
    }, {
      name: 'Reason 3',
      y: state.reason3,
      color: reason3
    }, {
      name: 'Reason 4',
      y: state.reason4,
      color: reason4
    }, {
      name: 'Reason 5',
      y: state.reason5,
      color: reason5
    },
    {
      name: 'Reason 6',
      y: state.reason6,
      color: reason6
    },
    {
      name: 'Reason 7',
      y: state.reason7,
      color: reason7
    },
    {
      name: 'Reason 8',
      y: state.reason8,
      color: reason8
    }],
    center: {
      lat: centerLat + (pieOffset.lat || 0),
      lon: centerLon + (pieOffset.lon || 0)
    }
  }, false);

  // Draw connector to state center if the pie has been offset
  if (pieOffset.drawConnector !== false) {
    var centerPoint = chart.fromLatLonToPoint({
        lat: centerLat,
        lon: centerLon
      }),
      offsetPoint = chart.fromLatLonToPoint({
        lat: centerLat + (pieOffset.lat || 0),
        lon: centerLon + (pieOffset.lon || 0)
      });
    chart.series[2].addPoint({
      name: state.id,
      path: 'M' + offsetPoint.x + ' ' + offsetPoint.y +
        'L' + centerPoint.x + ' ' + centerPoint.y
    }, false);
  }
});
// Only redraw once all pies and connectors have been added
chart.redraw();
