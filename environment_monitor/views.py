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
from django.views.decorators.csrf import csrf_exempt
# Python imports
import pytz
import json
import os
from uuid import uuid4
import time
# Project imports
from .models import *
#from .serializers import TemperatureSerializer,HumiditySerializer

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


# GET DATA FUNCTIONS
######################################################
@csrf_exempt
def get_device_data(request):
    """ get_device_data: Gets device data
    """
    dataset = [Device.objects.get(device_name="iot_ms")]
    json_response = serializers.serialize('json', dataset)
    return JsonResponse(json_response, safe=False)
