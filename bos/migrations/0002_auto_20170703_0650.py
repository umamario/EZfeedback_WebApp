# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-07-03 06:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bos', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trade',
            old_name='sell_currency',
            new_name='buy_currency',
        ),
    ]