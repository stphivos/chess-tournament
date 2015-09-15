# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('judge_interface', '0002_participant_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='date',
            field=models.DateField(default=datetime.datetime(2015, 9, 12, 20, 36, 14, 827396, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tournament',
            name='date',
            field=models.DateField(default=datetime.datetime(2015, 9, 12, 20, 36, 23, 755898, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
