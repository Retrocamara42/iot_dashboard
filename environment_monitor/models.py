from django.db import models
from django.utils import timezone
# Create your models here.
"""
Temperature:
    - id: Int. Id
    - timestamp: Datetime. Datetime when it was registered
    - temperature: Decimal. Temperature value
"""
class Temperature(models.Model):
    id=models.BigAutoField(primary_key=True)
    timestamp=models.DateTimeField(default=timezone.now)
    temperature=models.DecimalField(max_digits=5,decimal_places=2)

    class Meta:
        db_table = 'temperature'


"""
Humidity:
    - id: Int. Id
    - timestamp: Datetime. Datetime when it was registered
    - humidity: Decimal. Humidity value
"""
class Humidity(models.Model):
    id=models.BigAutoField(primary_key=True)
    timestamp=models.DateTimeField(default=timezone.now)
    humidity=models.DecimalField(max_digits=5,decimal_places=2)

    class Meta:
        db_table = 'humidity'
