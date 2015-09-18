# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('judge_interface', '0021_tournament_winner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='winner',
            field=models.ForeignKey(related_name='tournaments_won', blank=True, to='judge_interface.Participant', null=True),
        ),
    ]
