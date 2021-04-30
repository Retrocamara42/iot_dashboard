function jsChartReformatSoundRecordedJson(json_data){
   new_format_data={}
   labels=[]
   amplitudes=[]
   for(let record of JSON.parse(json_data)){
      labels.push(record['fields']['timestamp'])
      amplitudes.push(record['fields']['amplitude'])
   }
   amplitudes=[{
      label:'Amplitude',
      data: amplitudes,
      borderColor: 'rgb(192, 10, 10)',
      backgroundColor: 'rgb(192, 10, 10)',
   }]
   console.log(amplitudes)
   new_format_data['labels']=labels
   new_format_data['datasets']=amplitudes
   console.log(new_format_data)
   return new_format_data
}

function drawChart(data){
    var ctx = $("#audio_data");
    data=jsChartReformatSoundRecordedJson(data);
    var newChart = new Chart(ctx, {
       type: 'line',
       data: data,
       options: {
          responsive: true,
          maintainAspectRatio: true,
          scales: {
              yAxes: [{
                  ticks: {
                      beginAtZero:true
                  }
              }]
          }
       }
    })
}
$(document).ready(function() {
    data = $.ajax({
        url: "/sound_recorder/get_data_sound/",
        dataType:"json",
        async: true,
        success: function (data) {
            drawChart(data);
        }
    }).responseText});
