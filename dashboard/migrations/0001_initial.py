# Generated by Django 3.0.3 on 2020-04-15 15:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('conducteur', '0005_messageprobleme_solved'),
        ('vehicule', '0004_auto_20200414_2126'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('is_ct', models.BooleanField(default=False)),
                ('is_entretien_date', models.BooleanField(default=False)),
                ('is_entretien_km', models.BooleanField(default=False)),
                ('seen', models.BooleanField(default=False)),
                ('id_message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='conducteur.MessageProbleme')),
                ('id_vehicule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vehicule.Vehicule')),
            ],
        ),
    ]