from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import *
import pytz
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core import serializers
from django.http import JsonResponse
#from rest_framework import viewsets

# Create your views here.
"""
SoundRecorderHomeView: Main view of app sound recorder
"""
class SoundRecorderHomeView(TemplateView):
    template_name = "sound_recorder/soundrecorder_home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def get_audio_data(request):
    dataset = SoundRecorded.objects.all()
    json_response = serializers.serialize('json', dataset)
    return JsonResponse(json_response, safe=False)


"""
ReceiveSoundApi: API to receive and save sound detected
"""
class ReceiveSoundApi(APIView):

    def post(self, request):
        amplitude=request.POST["amplitude"]
        try:
            amplitude=float(amplitude)
        except Exception as e:
            raise ValidationError("El valor debe ser un número flotante válido")

        timezone.activate(pytz.timezone('America/Lima'))
        SoundRecorded.objects.create(amplitude=amplitude)
        timezone.deactivate()
        return JsonResponse({"message": "Valor de amplitud agregado exitosamente"})
