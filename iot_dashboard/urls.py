"""iot_dashboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
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
    path('environment_monitor/receive_temperature/', env_monitor.TemperatureApi.as_view()),
    path('environment_monitor/get_temperature_data/', env_monitor.get_temperature_data, name="get_temperature_data"),
    #### Environment monitor - humidity
    path('environment_monitor/receive_humidity/', env_monitor.HumidityApi.as_view()),
    path('environment_monitor/get_humidity_data/', env_monitor.get_humidity_data, name="get_humidity_data"),
]
