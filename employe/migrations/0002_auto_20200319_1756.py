# Generated by Django 3.0.3 on 2020-03-19 17:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employe', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='conduire',
            old_name='date_restit',
            new_name='date_et_temps_de_restitution',
        ),
        migrations.RemoveField(
            model_name='conduire',
            name='date_prise',
        ),
        migrations.AddField(
            model_name='conduire',
            name='date_et_temps_de_prise',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 19, 17, 56, 20, 522301)),
        ),
    ]
