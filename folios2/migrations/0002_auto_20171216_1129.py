# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-12-16 17:29
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('folios2', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='added',
            field=models.DateField(default=datetime.datetime(2017, 12, 16, 17, 29, 29, 910131, tzinfo=utc), verbose_name='added'),
        ),
    ]
