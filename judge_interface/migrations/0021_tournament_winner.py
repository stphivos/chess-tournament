# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('judge_interface', '0020_auto_20150917_1308'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='winner',
            field=models.ForeignKey(related_name='tournaments_won', to='judge_interface.Participant', null=True),
        ),
    ]
