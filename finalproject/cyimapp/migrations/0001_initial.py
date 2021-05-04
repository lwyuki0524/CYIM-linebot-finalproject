# Generated by Django 3.2 on 2021-04-30 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='foodTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fName', models.CharField(max_length=20)),
                ('fFoodImage', models.ImageField(upload_to='image/food/')),
                ('fMenuImage', models.ImageField(upload_to='image/menu/')),
                ('fPhone', models.CharField(blank=True, default='', max_length=20)),
                ('fAddress', models.CharField(blank=True, default='', max_length=255)),
            ],
        ),
    ]
