"""iot_dashboard URL Configuration
"""
from django.contrib import admin
from django.urls import path
import sound_recorder.views as sound_recorder
import environment_monitor.views as env_monitor

urlpatterns = [
    path('admin/', admin.site.urls),
    #### Sound recorder
    path('sound_recorder/home/', sound_recorder.SoundRecorderHomeView.as_view()),
    path('sound_recorder/receive_sound/', sound_recorder.ReceiveSoundApi.as_view()),
    path('sound_recorder/get_audio_data/', sound_recorder.get_audio_data, name="get_audio_data"),
    #### Environment monitor - temperature
    path('environment_monitor/home/', env_monitor.EnvironmentMonitorHomeView.as_view()),
    path('environment_monitor/get_temperature_data/', env_monitor.get_temperature_data, name="get_temperature_data"),
    #### Environment monitor - humidity
    path('environment_monitor/get_humidity_data/', env_monitor.get_humidity_data, name="get_humidity_data"),
]
