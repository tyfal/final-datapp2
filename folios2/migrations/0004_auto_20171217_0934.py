# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-12-17 15:34
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('folios2', '0003_auto_20171216_1905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='added',
            field=models.DateField(default=datetime.datetime(2017, 12, 17, 15, 34, 36, 861755, tzinfo=utc), verbose_name='added'),
        ),
        migrations.AlterField(
            model_name='stock',
            name='income_statement_10k',
            field=models.CharField(blank=True, max_length=100000, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='income_statement_10q',
            field=models.CharField(blank=True, max_length=100000, null=True),
        ),
    ]
