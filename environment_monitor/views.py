from django.shortcuts import render

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
        temperature=request.POST["temperature"]
        try:
            temperature=float(temperature)
        except Exception as e:
            raise ValidationError("La temperatura debe ser un valor válido flotante")

        timezone.activate(pytz.timezone('America/Lima'))
        Temperature.objects.create(temperature=temperature)
        timezone.deactivate()
        return JsonResponse({"message": "Valor de temperatura agregado exitosamente"})


"""
HumidityApi: API to receive and save humidity values
"""
class HumidityApi(APIView):

    def post(self, request):
        humidity=request.POST["humidity"]
        try:
            humidity=float(humidity)
        except Exception as e:
            raise ValidationError("La humedad debe ser un valor válido flotante")

        timezone.activate(pytz.timezone('America/Lima'))
        Humidity.objects.create(humidity=humidity)
        timezone.deactivate()
        return JsonResponse({"message": "Valor de humedad agregado exitosamente"})