# Generated by Django 5.1.2 on 2024-10-16 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_collection', '0002_subwaydailytimeslotpassengerdifference'),
    ]

    operations = [
        migrations.AddField(
            model_name='subwaydailytimeslotpassengerdifference',
            name='latitude',
            field=models.FloatField(default=37.5665),
        ),
        migrations.AddField(
            model_name='subwaydailytimeslotpassengerdifference',
            name='longitude',
            field=models.FloatField(default=126.978),
        ),
    ]
