# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('judge_interface', '0012_auto_20150914_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='p1_end_elo',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='p1_start_elo',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='game',
            name='p2_end_elo',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='p2_start_elo',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='participant',
            name='rating',
            field=models.BigIntegerField(),
        ),
    ]
