# Generated by Django 3.0.3 on 2020-03-19 18:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employe', '0002_auto_20200319_1756'),
    ]

    operations = [
        migrations.RenameField(
            model_name='conduire',
            old_name='num_employe',
            new_name='id_employe',
        ),
        migrations.AlterField(
            model_name='conduire',
            name='date_et_temps_de_prise',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 19, 18, 17, 20, 302964)),
        ),
    ]
