// Create the chart
console.log(all_data);
Highcharts.chart('container', {
    chart: {
        type: 'column'
    },
    title: {
        text: 'Number of sms per city today'
    },
    subtitle: {
        text: 'Click the columns to view count of each postal code'
    },
    accessibility: {
        announceNewData: {
            enabled: true
        }
    },
    xAxis: {
        type: 'category'
    },
    yAxis: {
        title: {
            text: 'Number of SMS sent today'
        }

    },
    legend: {
        enabled: false
    },
    plotOptions: {
        series: {
            borderWidth: 0,
            dataLabels: {
                enabled: true,
                format: '{point.y}'
            }
        }
    },

    tooltip: {
        headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
        pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y}</b> SMS<br/>'
    },
    series: [
        {
            name: "Cities",
            colorByPoint: true,
            data: all_data.count_per_city_today
        }
    ],
    drilldown: {
        series: all_data.count_per_postal
    }
});
