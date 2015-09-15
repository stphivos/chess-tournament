# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import judge_interface.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('participant_1_score', models.IntegerField()),
                ('participant_1_rating', models.IntegerField()),
                ('participant_2_score', models.IntegerField()),
                ('participant_2_rating', models.IntegerField()),
            ],
            options={
                'db_table': 'chess_game',
            },
            bases=(judge_interface.models.ModelBase, models.Model),
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rating', models.IntegerField()),
            ],
            options={
                'db_table': 'chess_participant',
            },
            bases=(judge_interface.models.ModelBase, models.Model),
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rounds', models.IntegerField()),
                ('k_factor', models.IntegerField()),
            ],
            options={
                'db_table': 'chess_tournament',
            },
            bases=(judge_interface.models.ModelBase, models.Model),
        ),
        migrations.AddField(
            model_name='game',
            name='participant_1',
            field=models.ForeignKey(related_name='games_1', to='judge_interface.Participant'),
        ),
        migrations.AddField(
            model_name='game',
            name='participant_2',
            field=models.ForeignKey(related_name='games_2', to='judge_interface.Participant'),
        ),
        migrations.AddField(
            model_name='game',
            name='tournament',
            field=models.ForeignKey(to='judge_interface.Tournament'),
        ),
    ]
