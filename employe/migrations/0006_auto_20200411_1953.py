# Generated by Django 3.0.3 on 2020-04-11 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employe', '0005_auto_20200411_1951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conduire',
            name='km_prise',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]