from django.db import models
from django.utils import timezone
# Create your models here.
class Temperature(models.Model):
    """
    Temperature:
        - id: Int. Id
        - device_name: String. Name of the device
        - timestamp: Datetime. Datetime when it was registered
        - temperature: Decimal. Temperature value
    """
    id=models.BigAutoField(primary_key=True)
    device_name=models.CharField(max_length=10)
    timestamp=models.DateTimeField(default=timezone.now)
    temperature=models.DecimalField(max_digits=5,decimal_places=2)

    class Meta:
        db_table = 'temperature'


class Humidity(models.Model):
    """
    Humidity:
        - id: Int. Id
        - device_name: String. Name of the device
        - timestamp: Datetime. Datetime when it was registered
        - humidity: Decimal. Humidity value
    """
    id=models.BigAutoField(primary_key=True)
    device_name=models.CharField(max_length=10)
    timestamp=models.DateTimeField(default=timezone.now)
    humidity=models.DecimalField(max_digits=5,decimal_places=2)

    class Meta:
        db_table = 'humidity'


class Pressure(models.Model):
    """
    Pressure:
        - id: Int. Id
        - device_name: String. Name of the device
        - timestamp: Datetime. Datetime when it was registered
        - pressure: Decimal. Pressure value
    """
    id=models.BigAutoField(primary_key=True)
    device_name=models.CharField(max_length=10)
    timestamp=models.DateTimeField(default=timezone.now)
    pressure=models.DecimalField(max_digits=5,decimal_places=2)

    class Meta:
        db_table = 'pressure'


class Device(models.Model):
    """
    Device:
        - id: Int. Id
        - device_name: String. Name of the device
        - token: String. Token to validate device
        - sent_frequency: Int. Frequency in minutes to send messages
    """
    id=models.BigAutoField(primary_key=True)
    device_name=models.CharField(max_length=10)
    token=models.CharField(max_length=35)
    sent_frequency=models.IntegerField()

    class Meta:
        db_table = 'device'
