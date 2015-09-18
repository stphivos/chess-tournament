# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('judge_interface', '0022_auto_20150917_1510'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='p1',
            field=models.ForeignKey(related_name='games_1', default=1, to='judge_interface.Participant'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='game',
            name='p2',
            field=models.ForeignKey(related_name='games_2', to='judge_interface.Participant', null=True),
        ),
    ]
