# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('judge_interface', '0019_auto_20150917_1124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='p1_score',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='p1_total_score',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='p2_score',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='p2_total_score',
            field=models.FloatField(null=True),
        ),
    ]
