# Generated by Django 3.2 on 2021-04-30 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cyimapp', '0004_remove_foodtable_fphone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodtable',
            name='fFoodImage',
            field=models.ImageField(null=True, upload_to='image/food/'),
        ),
        migrations.AlterField(
            model_name='foodtable',
            name='fMenuImage',
            field=models.ImageField(null=True, upload_to='image/menu/'),
        ),
    ]
