# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-10-23 00:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myuser', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='token',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
