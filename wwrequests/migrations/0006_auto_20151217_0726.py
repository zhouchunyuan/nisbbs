# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-16 23:26
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wwrequests', '0005_votes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='votes',
            name='id',
        ),
        migrations.AlterField(
            model_name='votes',
            name='username',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]