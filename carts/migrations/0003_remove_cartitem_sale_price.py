# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-20 13:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0002_cartitem_sale_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='sale_price',
        ),
    ]
