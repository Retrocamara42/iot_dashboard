"""iot_dashboard URL Configuration
"""
from django.contrib import admin
from django.urls import path
import home.views as home
import sound_recorder.views as sound_recorder
import environment_monitor.views as env_monitor
import AniM5Stack.views as anim5_stack


urlpatterns = [
    path('admin/', admin.site.urls),
    ### Home
    path('', home.HomeView.as_view(), name="home"),
    path('devices/', home.DeviceView.as_view(), name="devices"),
    path('home/get_device_data/', env_monitor.get_device_data),
    #### Environment monitor
    path('environment_monitor/dashboard/', env_monitor.EnvironmentMonitorDashboardView.as_view(), name="env_monitor"),
    path('environment_monitor/control/', env_monitor.EnvironmentMonitorControlView.as_view()),
    ### AniM5Stack
    path('anim5_stack/sd_manager/', anim5_stack.Anim5SDManagerView.as_view()),
    path('anim5_stack/load_sd_info/', anim5_stack.get_sd_info, name="get_sd_info"),
    path('anim5_stack/sd_file/', anim5_stack.post_sd_file, name="post_sd_file"),
]
