from django.db import models
from django.utils import timezone
# Create your models here.
"""
Temperature:
    - id: Int. Id
    - device_name: String. Name of the device
    - timestamp: Datetime. Datetime when it was registered
    - temperature: Decimal. Temperature value
"""
class Temperature(models.Model):
    id=models.BigAutoField(primary_key=True)
    device_name=models.CharField(max_length=10)
    timestamp=models.DateTimeField(default=timezone.now)
    temperature=models.DecimalField(max_digits=5,decimal_places=2)

    class Meta:
        db_table = 'temperature'


"""
Humidity:
    - id: Int. Id
    - device_name: String. Name of the device
    - timestamp: Datetime. Datetime when it was registered
    - humidity: Decimal. Humidity value
"""
class Humidity(models.Model):
    id=models.BigAutoField(primary_key=True)
    device_name=models.CharField(max_length=10)
    timestamp=models.DateTimeField(default=timezone.now)
    humidity=models.DecimalField(max_digits=5,decimal_places=2)

    class Meta:
        db_table = 'humidity'


"""
Device:
    - id: Int. Id
    - device_name: String. Name of the device
    - sent_frequency: Int. Frequency in minutes to send messages
"""
class Device(models.Model):
    id=models.BigAutoField(primary_key=True)
    device_name=models.CharField(max_length=10)
    sent_frequency=models.IntegerField()

    class Meta:
        db_table = 'device'
