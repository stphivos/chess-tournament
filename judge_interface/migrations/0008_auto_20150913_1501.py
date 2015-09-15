# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import judge_interface.models


class Migration(migrations.Migration):

    dependencies = [
        ('judge_interface', '0007_auto_20150913_1156'),
    ]

    operations = [
        migrations.CreateModel(
            name='TournamentParticipant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('participant', models.ForeignKey(to='judge_interface.Participant')),
                ('tournament', models.ForeignKey(to='judge_interface.Tournament')),
            ],
            options={
                'db_table': 'chess_tournament_participant',
            },
            bases=(judge_interface.models.ModelBase, models.Model),
        ),
        migrations.AddField(
            model_name='tournament',
            name='participants',
            field=models.ManyToManyField(to='judge_interface.Participant', through='judge_interface.TournamentParticipant'),
        ),
    ]
