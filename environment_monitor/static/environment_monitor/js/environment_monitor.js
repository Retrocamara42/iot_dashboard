$(document).ready(function() {
    data = $.ajax({
        url: "/environment_monitor/get_temperature/",
        dataType:"json",
        async: true,
        success: function (data) {
           drawChart(data, '#temperature', 'temperature', 'humidity',
                    'rgb(192, 10, 10)', 'rgb(192, 10, 10)');
        }
    }).responseText});
