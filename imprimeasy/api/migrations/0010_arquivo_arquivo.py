# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-11-07 11:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20181023_1024'),
    ]

    operations = [
        migrations.AddField(
            model_name='arquivo',
            name='arquivo',
            field=models.FileField(default='Arquivo mão encontrado', upload_to=''),
        ),
    ]
