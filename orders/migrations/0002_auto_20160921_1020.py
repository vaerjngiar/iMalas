# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-21 07:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraddress',
            name='phone',
            field=models.CharField(default=11111, max_length=120),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usercheckout',
            name='phone',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
