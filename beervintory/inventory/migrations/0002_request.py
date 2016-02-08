# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-06 10:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('style', models.CharField(default='Style', max_length=50, unique=True)),
                ('brewer', models.CharField(default='Brewer', max_length=50, unique=True)),
            ],
        ),
    ]
