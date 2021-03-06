# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-04 00:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Arquivo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('local', models.CharField(max_length=200)),
                ('status', models.IntegerField(choices=[(1, 'Impresso'), (2, 'Aguardando aprovação'), (3, 'Impressão negada')], default=2)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matricula', models.CharField(max_length=30)),
                ('nome', models.CharField(max_length=200)),
                ('senha', models.CharField(max_length=200)),
                ('saldo', models.FloatField(default=0.0)),
            ],
        ),
        migrations.AddField(
            model_name='arquivo',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Usuario'),
        ),
    ]
