# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('judge_interface', '0003_auto_20150912_2036'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='date',
        ),
        migrations.RemoveField(
            model_name='tournament',
            name='date',
        ),
        migrations.AddField(
            model_name='game',
            name='end_date',
            field=models.DateField(default=datetime.datetime.now, blank=True),
        ),
        migrations.AddField(
            model_name='game',
            name='start_date',
            field=models.DateField(default=datetime.datetime.now, blank=True),
        ),
        migrations.AddField(
            model_name='tournament',
            name='end_date',
            field=models.DateField(default=datetime.datetime.now, blank=True),
        ),
        migrations.AddField(
            model_name='tournament',
            name='start_date',
            field=models.DateField(default=datetime.datetime.now, blank=True),
        ),
    ]
