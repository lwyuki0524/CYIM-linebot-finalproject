# Generated by Django 3.2.3 on 2021-05-16 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cyimapp', '0012_auto_20210515_2023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodtable',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
