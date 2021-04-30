from django.db import models

# Create your models here.
class SoundRecorded(models.Model):
    id=models.BigAutoField(primary_key=True)
    timestamp=models.DateTimeField(auto_now_add=True)
    amplitude=models.DecimalField(max_digits=5,decimal_places=2)
