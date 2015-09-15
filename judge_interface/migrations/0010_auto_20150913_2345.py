# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('judge_interface', '0009_auto_20150913_1638'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='p1_score',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='p2_score',
            field=models.IntegerField(null=True),
        ),
    ]
