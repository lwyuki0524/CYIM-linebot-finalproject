# Generated by Django 2.2.5 on 2021-05-02 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cyimapp', '0007_auto_20210502_1341'),
    ]

    operations = [
        migrations.AddField(
            model_name='foodtable',
            name='fMenuImage',
            field=models.ImageField(default='', null=True, upload_to='image/menu/'),
        ),
    ]
