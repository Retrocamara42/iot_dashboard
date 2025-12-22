from rest_framework import serializers
from .models import Temperature,Humidity,Pressure

class TemperatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Temperature
        fields = ['temperature'] # used?


class ApiTemperatureSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Temperature
        fields = ['timestamp','temperature']


class HumiditySerializer(serializers.ModelSerializer):
    class Meta:
        model = Humidity
        fields = ['humidity']



class PressureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pressure
        fields = ['pressure']
