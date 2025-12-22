# Django imports
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.http import JsonResponse
from django.core import serializers
from rest_framework import permissions, viewsets
from django.views.decorators.csrf import csrf_exempt
# Python imports
from uuid import uuid4
# Project imports
from .models import *
from .serializers import ApiTemperatureSerializer#,HumiditySerializer

# VIEWS
######################################################
class EnvironmentMonitorDashboardView(TemplateView):
    """ EnvironmentMonitorDashboardView: Dashboard view of app environemnt monitor
    """
    template_name = "environment_monitor/environment_monitor_home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class EnvironmentMonitorControlView(TemplateView):
    """ EnvironmentMonitorControlView: Control view of app environemnt monitor
    """
    template_name = "environment_monitor/environment_monitor_control.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

# API VIEWS
class TemperatureViewApi(viewsets.ModelViewSet):
    """ API endpoint to get last temperature value
    """
    queryset = Temperature.objects.all().filter(timestamp=Temperature.objects.order_by("-timestamp").first().timestamp)
    serializer_class = ApiTemperatureSerializer
    permission_classes = [permissions.IsAuthenticated]


# GET DATA FUNCTIONS
######################################################
@csrf_exempt
def get_device_data(request):
    """ get_device_data: Gets device data
    """
    dataset = [Device.objects.get(device_name="iot_ms")]
    json_response = serializers.serialize('json', dataset)
    return JsonResponse(json_response, safe=False)
