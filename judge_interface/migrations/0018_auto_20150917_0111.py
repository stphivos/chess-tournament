# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('judge_interface', '0017_auto_20150914_2035'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='p1_end_elo',
        ),
        migrations.RemoveField(
            model_name='game',
            name='p1_start_elo',
        ),
        migrations.RemoveField(
            model_name='game',
            name='p2_end_elo',
        ),
        migrations.RemoveField(
            model_name='game',
            name='p2_start_elo',
        ),
        migrations.AddField(
            model_name='game',
            name='p1_total_score',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='p2_total_score',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='p1',
            field=models.ForeignKey(related_name='games_1', to='judge_interface.Participant', null=True),
        ),
    ]
