from rest_framework import serializers
from .models import Temperature,Humidity,Pressure

class ApiTemperatureSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Temperature
        fields = ['timestamp','temperature']

