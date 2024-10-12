
function jsChartReformatMeasurementJson(json_data, measurement_label, label_name,
         border_color, background_color){
   new_format_data={};
   labels=[];
   measurement=[];
   var min=999;
   var max=-999;
   for(let record of JSON.parse(json_data)){
      measure=record['fields'][measurement_label]
      min = measure<min ? measure:min; 
      max = measure>max ? measure:max; 
      labels.push(record['fields']['timestamp']);
      measurement.push(measure);
   }
   measurement=[{
      label:label_name,
      data: measurement,
      borderColor: border_color,
      backgroundColor: background_color,
   }];
   new_format_data['labels']=labels;
   new_format_data['datasets']=measurement;
   return {new_format_data, min, max};
}

function drawChart(data, chart_id, measurement_label, label_name,
         border_color, background_color, units){
    var ctx = $(chart_id);
    var pad = 4;
    var result=jsChartReformatMeasurementJson(data, measurement_label, 
            label_name, border_color, background_color);
    var data=result.new_format_data;
    var min=result.min;
    var max=result.max;
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
             mode: 'x',
             callbacks: {
                 label: function(tooltipItems, data) {
                     return tooltipItems.yLabel + ' ' + units;
                 }
             }
          },
          scales: {
            x: {
              type: 'time',
              time: {
                  parser: 'Y-M-D hh:mm:ss',
                  unit:'minute',
                  displayFormats: {
                     minute: 'Y-M-D hh:mm:ss'
                  }
              },
              ticks: {
                color: '#49515c',
                autoSkip: true,
                maxTicksLimit: 15
              }
            },
            y: {
               suggestedMin: min-pad,
               suggestedMax: max+pad,
            }
         },
         plugins: {
            legend: {
                display: true,
                position:'bottom'
            }
         }
       }
    })
    return newChart;
}
