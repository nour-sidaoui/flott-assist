# Generated by Django 3.0.3 on 2020-04-15 18:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_auto_20200415_1822'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='notification',
            table='dashboard_notification',
        ),
    ]
