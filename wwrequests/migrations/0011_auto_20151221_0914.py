# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-21 01:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wwrequests', '0010_requests_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requests',
            name='score',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]