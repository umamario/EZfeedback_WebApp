# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2018-03-24 20:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bos', '0006_auto_20180324_1524'),
    ]

    operations = [
        migrations.AddField(
            model_name='companypartner',
            name='name',
            field=models.TextField(max_length=40, null=True),
        ),
    ]