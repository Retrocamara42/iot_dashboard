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
get_temperature_data: Gets temperature data
"""
def get_temperature_data(request):
    try:
        max_points=request.POST.get("puntos_temp", 0)
        if(max_points!=0):
            max_points=int(max_points)
    except Exception as e:
        print("Error while getting value puntos_temp: "+str(e))
        max_points=0
    dataset = Temperature.objects.all().order_by('-id')[:max_points]
    json_response = serializers.serialize('json', dataset)
    return JsonResponse(json_response, safe=False)


"""
get_humidity_data: Gets humidity data
"""
def get_humidity_data(request):
    try:
        max_points=request.POST.get("puntos_humid", 0)
        if(max_points!=0):
            max_points=int(max_points)
    except Exception as e:
        print("Error while getting value puntos_humid: "+str(e))
        max_points=0
    dataset = Humidity.objects.all().order_by('-id')[:max_points]
    json_response = serializers.serialize('json', dataset)
    return JsonResponse(json_response, safe=False)


"""
get_device_data: Gets device data
"""
def get_device_data(request):
    dataset = [Device.objects.get(device_name="iot_ms")]
    json_response = serializers.serialize('json', dataset)
    return JsonResponse(json_response, safe=False)



# COMMAND FUNCTIONS
######################################################
"""
publish_message: Publish message in json format to mqtt's topic
"""
def publish_message(topic, message_json):
    try:
        event_loop_group = io.EventLoopGroup(1)
        host_resolver = io.DefaultHostResolver(event_loop_group)
        client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
        mqtt_connection = mqtt_connection_builder.mtls_from_path(
                endpoint=os.getenv('MQTT_ENDPOINT'),
                port=int(os.getenv('MQTT_PORT')),
                cert_filepath="./certs/iot_multisensor_certificate.pem.crt",
                pri_key_filepath="./certs/iot_multisensor_private.pem.key",
                ca_filepath="./certs/AmazonRootCA1.pem",
                client_bootstrap=client_bootstrap,
                clean_session=False,
                client_id="iot-" + str(uuid4()),
                keep_alive_secs=6,)
        connect_future = mqtt_connection.connect()
        connect_future.result()

        mqtt_connection.publish(
            topic=topic,
            payload=message_json,
            qos=mqtt.QoS.AT_LEAST_ONCE)
        time.sleep(1)

        disconnect_future = mqtt_connection.disconnect()
        disconnect_future.result()
        return_message="Mensaje enviado al dispositivo exitosamente"
    except Exception as e:
        return_message="Error al publicar mensaje "+message_json+" al topico "+topic+": "+str(e)
        print(return_message)
        try:
            disconnect_future = mqtt_connection.disconnect()
            disconnect_future.result()
        except Exception as e:
            return_message="Error al desconectar de mqtt: "+str(e)
            print(return_message)

    return return_message



"""
query_device: Query command that tells device to send data
"""
def query_device(request):
    topic="remote_action"
    message = {"q":1}
    message_json = json.dumps(message)
    print("Publishing message to topic '{}': {}".format(topic, message))
    return_message=publish_message(topic, message_json)

    return JsonResponse({'response': return_message})



"""
set_sent_frequency: Send new sent frequency value for iot device
"""
def set_sent_frequency(request):
    topic="remote_action"
    try:
        freq=int(request.POST.get("freq", 30))
    except Exception as e:
        return JsonResponse({'response': "Error: Value can't be parsed as int"})
    if(freq<0 or freq>999):
        return JsonResponse({'response': 'Error: Value of sent frequency must be greater than 0 and less than 999'})
    message = {"f":freq}
    message_json = json.dumps(message)
    print("Publishing message to topic '{}': {}".format(topic, message))
    return_message=publish_message(topic, message_json)

    return JsonResponse({'response': return_message})



# NOT USED
######################################################
"""
TemperatureApi: API to receive and save temperature values

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
