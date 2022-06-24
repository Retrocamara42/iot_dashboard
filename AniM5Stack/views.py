from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.http import JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from .models import *

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
    """ get_sd_info: Gets sd info
    """
    record = SdInfo.objects.get(device_name="anim5")
    json_response = serializers.serialize('json', record)
    return JsonResponse(json_response, safe=False)