# Generated by Django 3.0.3 on 2020-03-12 15:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Vehicule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marque', models.CharField(max_length=255)),
                ('modele', models.CharField(max_length=255)),
                ('annee', models.IntegerField()),
                ('immat', models.CharField(max_length=9)),
                ('couleur', models.CharField(max_length=255)),
                ('km', models.IntegerField()),
                ('disponible', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Entretien',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('montant', models.FloatField()),
                ('id_vehicule', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='vehicule.Vehicule')),
            ],
        ),
    ]
