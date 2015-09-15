# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('judge_interface', '0010_auto_20150913_2345'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='no',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
