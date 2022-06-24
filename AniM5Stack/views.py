from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.http import JsonResponse
from django.core import serializers
from .models import *

# VIEWS
######################################################
"""
Anim5SDManagerView: SD Manager view of app Anim5Stack
"""
class Anim5SDManagerView(TemplateView):
    template_name = "AniM5Stack/anim5_sdmanager.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context



# GET DATA FUNCTIONS
######################################################
"""
get_sd_info: Gets sd info
"""
def get_sd_info(request):
    record = SdInfo.objects.get(device_name="anim5")
    json_response = serializers.serialize('json', record)
    return JsonResponse(json_response, safe=False)