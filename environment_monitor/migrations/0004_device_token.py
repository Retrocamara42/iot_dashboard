# Generated by Django 3.2.9 on 2022-08-12 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('environment_monitor', '0003_device'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='token',
            field=models.CharField(default='0k25YEmxDU-xOHRqR6VZH-b0bZmnvCRt', max_length=35),
            preserve_default=False,
        ),
    ]
