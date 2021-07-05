
function jsChartReformatMeasurementJson(json_data, measurement_label, label_name,
         border_color, background_color){
   new_format_data={}
   labels=[]
   measurement=[]
   for(let record of JSON.parse(json_data)){
      labels.push(record['fields']['timestamp'])
      measurement.push(record['fields'][measurement_label])
   }
   measurement=[{
      label:label_name,
      data: measurement,
      borderColor: border_color,
      backgroundColor: background_color,
   }]
   new_format_data['labels']=labels
   new_format_data['datasets']=measurement
   return new_format_data
}

function drawChart(data, chart_id, measurement_label, label_name,
         border_color, background_color, units){
    var ctx = $(chart_id);
    data=jsChartReformatMeasurementJson(data, measurement_label, label_name,
             border_color, background_color);
    var newChart = new Chart(ctx, {
       type: 'line',
       data: data,
       options: {
          responsive: true,
          maintainAspectRatio: true,
          interaction: {
            intersect: false
          },
          tooltips: {
             position : 'nearest',
             enabled: true,
             mode: 'point',
             callbacks: {
                 label: function(tooltipItems, data) {
                     return tooltipItems.yLabel + ' ' + units;
                 }
             }
          },
          xAxes: [{
             type: 'time',
             ticks: {
                 autoSkip: true,
                 maxTicksLimit: 5
             }
         }],
       }
    })
}
