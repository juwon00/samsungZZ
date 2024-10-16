# Generated by Django 5.1.2 on 2024-10-16 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_collection', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DegreeOfSubwayCongestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_name', models.CharField(max_length=20)),
                ('sub_num', models.IntegerField()),
                ('route_name', models.CharField(max_length=20)),
                ('week', models.CharField(max_length=10)),
                ('time', models.CharField(max_length=10)),
                ('congestion', models.FloatField(null=True)),
            ],
            options={
                'db_table': 'degree_of_subway_congestion',
            },
        ),
    ]
