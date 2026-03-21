from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.http import JsonResponse
from django.core import serializers
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from environment_monitor.models import *

# VIEWS
######################################################
"""
HomeView: Home view of underground cuy
"""
class HomeView(TemplateView):
    template_name = "home/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


"""
DeviceView: Devices' view of underground cuy
"""
class DeviceView(TemplateView):
    template_name = "home/devices.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


"""
DashboardView: Summary of data of underground cuy
"""
class DashboardView(TemplateView):
    template_name = "home/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# GET DATA FUNCTIONS
######################################################
@csrf_exempt
def get_dashboard_data(request):
    """ get_dashboard_data: Gets dashboard data
    """
    if request.method == "GET":
        esp_temp = Temperature.objects.all().filter(device_name=VALID_ENV_DEVICES[0]
                    ).order_by("-timestamp").first().temperature
        esp_humid = Humidity.objects.all().filter(device_name=VALID_ENV_DEVICES[0] 
                    ).order_by("-timestamp").first().humidity
        m5_temp = Temperature.objects.all().filter(device_name=VALID_ENV_DEVICES[1] 
                    ).order_by("-timestamp").first().temperature
        m5_humid = Humidity.objects.all().filter(device_name=VALID_ENV_DEVICES[1]
                    ).order_by("-timestamp").first().humidity
        m5_press = Pressure.objects.all().filter(device_name=VALID_ENV_DEVICES[1]
                    ).order_by("-timestamp").first().pressure
        response = {
            "esp":
                {"temp":esp_temp, "humid":esp_humid},
            "m5":
                {"temp":m5_temp, "humid":m5_humid, "press":m5_press}
            }
        return JsonResponse(response, safe=False)