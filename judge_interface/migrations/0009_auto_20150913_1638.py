# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('judge_interface', '0008_auto_20150913_1501'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='participant_1',
            new_name='p1',
        ),
        migrations.RenameField(
            model_name='game',
            old_name='participant_1_score',
            new_name='p1_score',
        ),
        migrations.RenameField(
            model_name='game',
            old_name='participant_1_rating',
            new_name='p1_start_elo',
        ),
        migrations.RenameField(
            model_name='game',
            old_name='participant_2',
            new_name='p2',
        ),
        migrations.RenameField(
            model_name='game',
            old_name='participant_2_score',
            new_name='p2_score',
        ),
        migrations.RenameField(
            model_name='game',
            old_name='participant_2_rating',
            new_name='p2_start_elo',
        ),
        migrations.AddField(
            model_name='game',
            name='p1_end_elo',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='p2_end_elo',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='round',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tournament',
            name='current_round',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='game',
            name='tournament',
            field=models.ForeignKey(related_name='games', to='judge_interface.Tournament'),
        ),
    ]
