from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.http import JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import os
import binascii
from uuid import uuid4
from .models import *
from environment_monitor.models import *
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Aws imports
from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder

from iot_dashboard.constants import *

# VIEWS
######################################################
class Anim5SDManagerView(TemplateView):
    """ Anim5SDManagerView: SD Manager view of app Anim5Stack
    """
    template_name = "AniM5Stack/anim5_sdmanager.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        if request.method == 'POST' and request.FILES['sd_file']:
            sd_file = request.FILES['sd_file']
            fs = FileSystemStorage()
            fs.save(sd_file.name, sd_file)

            event_loop_group = io.EventLoopGroup(1)
            host_resolver = io.DefaultHostResolver(event_loop_group)
            client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
            mqtt_connection = mqtt_connection_builder.mtls_from_path(
                    endpoint=os.getenv('MQTT_ENDPOINT'),
                    port=int(os.getenv('MQTT_PORT')),
                    cert_filepath=CERT_FILEPATH,
                    pri_key_filepath=PRI_KEY_FILEPATH,
                    ca_filepath=CA_FILEPATH,
                    client_bootstrap=client_bootstrap,
                    clean_session=False,
                    client_id="iot-" + str(uuid4()),
                    keep_alive_secs=6,)
            connect_future = mqtt_connection.connect()
            connect_future.result()

            token=Device.objects.get(device_name="anim5").token
            payload = '{{"dv":{},"tk":{},"fn":{}}}'.format(
                "anim5", token, sd_file.name)
            mqtt_connection.publish(
                topic="sd_file",                    
                payload=payload,
                qos=mqtt.QoS.AT_LEAST_ONCE)
            disconnect_future=mqtt_connection.disconnect()
            disconnect_future.result()
            return render(request, self.template_name)
        return render(request, self.template_name)


# GET DATA FUNCTIONS
######################################################
@csrf_exempt
def get_sd_info(request):
    """ get_sd_info: Gets sd info """
    record = [SdInfo.objects.get(device_name="anim5")]
    json_response = serializers.serialize('json', record)
    return JsonResponse(json_response, safe=False)


# POST FUNCTIONS
######################################################
@api_view(['POST'])
def post_sd_file(request):
    """ post_sd_file: Returns sd file """
    if request.method == "POST":
        device=request.POST.get("device")
        token=request.POST.get("token")
        filename=request.POST.get("filename")
        try:
            device = Device.objects.get(device_name=device)
        except Exception as e:
            device = None
        if device is not None:
            if device.token==token:
                path_file=os.path.join(settings.MEDIA_ROOT,filename)
                with open(path_file, 'rb') as output:
                    content=output.readlines()
                content=b''.join(content)
                payload=binascii.b2a_hex(content)
                os.remove(path_file)
                return Response(payload, status=status.HTTP_200_OK)
        return Response('{{"error":{}}}'.format(
            "Device doesn't go with said token"), 
            status=status.HTTP_400_BAD_REQUEST)


