# Generated by Django 3.0.3 on 2020-04-28 18:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employe', '0006_auto_20200411_1953'),
        ('conducteur', '0005_messageprobleme_solved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messageprobleme',
            name='id_employe',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='employe.Employe'),
        ),
    ]
