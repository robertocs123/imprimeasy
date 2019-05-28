# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-10-23 13:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20181023_0856'),
    ]

    operations = [
        migrations.AddField(
            model_name='arquivo',
            name='obs',
            field=models.CharField(default='Sem obs.', max_length=1000),
        ),
        migrations.AddField(
            model_name='arquivo',
            name='valor',
            field=models.FloatField(default=0.0),
        ),
    ]