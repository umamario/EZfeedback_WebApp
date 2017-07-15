# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-07-15 11:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bos', '0005_auto_20170715_1043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trade',
            name='buy_currency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buy_currency', to='bos.Currency'),
        ),
        migrations.AlterField(
            model_name='trade',
            name='sell_currency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sell_currency', to='bos.Currency'),
        ),
    ]