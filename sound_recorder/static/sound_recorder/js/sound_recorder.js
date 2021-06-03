$(document).ready(function() {
    data = $.ajax({
        url: "/sound_recorder/get_audio_data/",
        dataType:"json",
        async: true,
        success: function (data) {
           drawChart(data, "#audio_data", 'amplitude', 'Amplitude',
                    'rgb(192, 10, 10)', 'rgb(192, 10, 10)');
        }
    }).responseText});
