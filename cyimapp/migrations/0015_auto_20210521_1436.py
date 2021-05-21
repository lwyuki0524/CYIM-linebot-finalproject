# Generated by Django 3.1.4 on 2021-05-21 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cyimapp', '0014_auto_20210516_2346'),
    ]

    operations = [
        migrations.AddField(
            model_name='foodtable',
            name='fEndTime',
            field=models.TimeField(null=True),
        ),
        migrations.AddField(
            model_name='foodtable',
            name='fLatitude',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='foodtable',
            name='fLongitude',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='foodtable',
            name='fStartTime',
            field=models.TimeField(null=True),
        ),
    ]