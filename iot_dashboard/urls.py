"""iot_dashboard URL Configuration
"""
from django.contrib import admin
from django.urls import path
import home.views as home
import sound_recorder.views as sound_recorder
import environment_monitor.views as env_monitor

urlpatterns = [
    path('admin/', admin.site.urls),
    ### Home
    path('', home.HomeView.as_view(), name="home"),
    path('home/get_device_data/', env_monitor.get_device_data),
    #### Sound recorder
    path('sound_recorder/home/', sound_recorder.SoundRecorderHomeView.as_view()),
    path('sound_recorder/receive_sound/', sound_recorder.ReceiveSoundApi.as_view()),
    path('sound_recorder/get_audio_data/', sound_recorder.get_audio_data, name="get_audio_data"),
    #### Environment monitor
    path('environment_monitor/dashboard/', env_monitor.EnvironmentMonitorDashboardView.as_view(), name="env_monitor"),
    path('environment_monitor/control/', env_monitor.EnvironmentMonitorControlView.as_view()),
]
