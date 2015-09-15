# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('judge_interface', '0006_auto_20150913_1146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='end_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='end_date',
            field=models.DateTimeField(null=True),
        ),
    ]
