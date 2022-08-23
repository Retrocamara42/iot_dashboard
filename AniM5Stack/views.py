from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.http import JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from .models import *
from environment_monitor.models import *
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import os
import base64

# VIEWS
######################################################
class Anim5SDManagerView(TemplateView):
    """ Anim5SDManagerView: SD Manager view of app Anim5Stack
    """
    template_name = "AniM5Stack/anim5_sdmanager.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context



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
        try:
            device = Device.objects.get(device_name=device)
        except Exception as e:
            device = None
        if device is not None:
            if device.token==token:
                filename="prueba.bmp"
                path_file=os.path.join(settings.MEDIA_ROOT,filename)
                with open(path_file, 'rb') as output:
                    content=output.readlines()
                content=b''.join(content)
                #content=str(content, 'utf-8')
                payload='{}'.format(content)
                return Response(payload, status=status.HTTP_200_OK)
        return Response('{{"error":{}}}'.format(
            "Device doesn't go with said token"), 
            status=status.HTTP_400_BAD_REQUEST)