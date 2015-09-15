# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('judge_interface', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='name',
            field=models.CharField(default=datetime.datetime(2015, 9, 9, 20, 42, 28, 893068, tzinfo=utc), max_length=100),
            preserve_default=False,
        ),
    ]
