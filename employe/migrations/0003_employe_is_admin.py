# Generated by Django 3.0.3 on 2020-04-09 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employe', '0002_auto_20200405_2150'),
    ]

    operations = [
        migrations.AddField(
            model_name='employe',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
    ]
