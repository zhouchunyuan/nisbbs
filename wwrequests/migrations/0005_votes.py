# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-16 10:51
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wwrequests', '0004_auto_20151215_0753'),
    ]

    operations = [
        migrations.CreateModel(
            name='Votes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank1', models.ManyToManyField(related_name='r1', to='wwrequests.Requests')),
                ('rank2', models.ManyToManyField(related_name='r2', to='wwrequests.Requests')),
                ('rank3', models.ManyToManyField(related_name='r3', to='wwrequests.Requests')),
                ('rank4', models.ManyToManyField(related_name='r4', to='wwrequests.Requests')),
                ('rank5', models.ManyToManyField(related_name='r5', to='wwrequests.Requests')),
                ('username', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]