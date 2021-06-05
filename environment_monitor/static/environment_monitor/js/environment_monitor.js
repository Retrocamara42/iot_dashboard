$(document).ready(function() {
    data = $.ajax({
        url: "/environment_monitor/get_temperature_data/",
        dataType:"json",
        async: true,
        success: function (data) {
           drawChart(data, '#temperature', 'temperature', 'temperature',
                    'rgb(192, 10, 10)', 'rgb(192, 10, 10)');
        }
    }).responseText});


    $(document).ready(function() {
        data = $.ajax({
            url: "/environment_monitor/get_humidity_data/",
            dataType:"json",
            async: true,
            success: function (data) {
               drawChart(data, '#humidity', 'humidity', 'humidity',
                        'rgb(192, 10, 10)', 'rgb(192, 10, 10)');
            }
        }).responseText});
