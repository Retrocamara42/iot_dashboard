from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import *
import pytz
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TemperatureSerializer,HumiditySerializer
from django.http import JsonResponse
from rest_framework import status
from django.core import serializers

# Create your views here.
"""
EnvironmentMonitorHomeView: Main view of app environemnt monitor
"""
class EnvironmentMonitorHomeView(TemplateView):
    template_name = "environment_monitor/environment_monitor_home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def get_temperature_data(request):
    dataset = Temperature.objects.all()
    json_response = serializers.serialize('json', dataset)
    return JsonResponse(json_response, safe=False)


def get_humidity_data(request):
    dataset = Humidity.objects.all()
    json_response = serializers.serialize('json', dataset)
    return JsonResponse(json_response, safe=False)


"""
TemperatureApi: API to receive and save temperature values
"""
class TemperatureApi(APIView):

    def post(self, request):
        print(request.data)
        serializer = TemperatureSerializer(data=request.data)
        if(serializer.is_valid()):
            temperature=serializer.data["temperature"]
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        #raise ValidationError("La temperatura debe ser un valor válido flotante")

        timezone.activate(pytz.timezone('America/Lima'))
        Temperature.objects.create(temperature=temperature)
        timezone.deactivate()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


"""
HumidityApi: API to receive and save humidity values
"""
class HumidityApi(APIView):
    def post(self, request):
        print(request.data)
        serializer = HumiditySerializer(data=request.data)
        if(serializer.is_valid()):
            humidity=serializer.data["humidity"]
        else:
            print(serializer.data["humidity"])
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        timezone.activate(pytz.timezone('America/Lima'))
        Humidity.objects.create(humidity=humidity)
        timezone.deactivate()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
