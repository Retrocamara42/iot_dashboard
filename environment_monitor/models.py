from django.db import models

# Create your models here.
"""
Temperature:
    - id: Int. Id
    - timestamp: Datetime. Datetime when it was registered
    - temperature: Decimal. Temperature value
"""
class Temperature(models.Model):
    id=models.BigAutoField(primary_key=True)
    timestamp=models.DateTimeField(auto_now_add=True)
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
    timestamp=models.DateTimeField(auto_now_add=True)
    humidity=models.DecimalField(max_digits=5,decimal_places=2)

    class Meta:
        db_table = 'humidity'
