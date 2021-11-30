# Django imports
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.http import JsonResponse
from django.core import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Python imports
import pytz
import json
import os
from uuid import uuid4
import time
# Aws imports
from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
# Project imports
from .models import *
#from .serializers import TemperatureSerializer,HumiditySerializer

# VIEWS
######################################################
"""
EnvironmentMonitorDashboardView: Dashboard view of app environemnt monitor
"""
class EnvironmentMonitorDashboardView(TemplateView):
    template_name = "environment_monitor/environment_monitor_home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


"""
EnvironmentMonitorControlView: Control view of app environemnt monitor
"""
class EnvironmentMonitorControlView(TemplateView):
    template_name = "environment_monitor/environment_monitor_control.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# GET DATA FUNCTIONS
######################################################
"""
get_device_data: Gets device data
"""
def get_device_data(request):
    dataset = [Device.objects.get(device_name="iot_ms")]
    json_response = serializers.serialize('json', dataset)
    return JsonResponse(json_response, safe=False)
