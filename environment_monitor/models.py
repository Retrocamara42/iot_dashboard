from django.db import models

# Create your models here.
class Temperature(models.Model):
    id=models.BigAutoField(primary_key=True)
    timestamp=models.DateTimeField(auto_now_add=True)
    temperature=models.DecimalField(max_digits=5,decimal_places=2)

class Humidity(models.Model):
    id=models.BigAutoField(primary_key=True)
    timestamp=models.DateTimeField(auto_now_add=True)
    humidity=models.DecimalField(max_digits=5,decimal_places=2)
