# Generated by Django 3.0.3 on 2020-04-15 15:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vehicule', '0004_auto_20200414_2126'),
        ('dashboard', '0002_auto_20200415_1535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='id_vehicule',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='vehicule.Vehicule'),
        ),
    ]