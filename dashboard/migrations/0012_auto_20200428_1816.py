# Generated by Django 3.0.3 on 2020-04-28 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0011_auto_20200415_2132'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='diff',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='is_diff',
            field=models.BooleanField(default=False),
        ),
    ]
