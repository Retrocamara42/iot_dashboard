from django.db import models
from django.utils import timezone
# Create your models here.
class SdInfo(models.Model):
    """
    SdInfo:
        - device_name: String. Name of the device
        - timestamp: Datetime. Datetime when it was registered
        - total_storage: Integer. Total storage
        - free_storage: Integer. Free storage
        - used_storage: Integer. Used storage
    """
    device_name=models.CharField(primary_key=True,max_length=10)
    timestamp=models.DateTimeField(default=timezone.now)
    total_storage=models.BigIntegerField()
    free_storage=models.BigIntegerField()
    used_storage=models.BigIntegerField()

    class Meta:
        db_table = 'sd_info'