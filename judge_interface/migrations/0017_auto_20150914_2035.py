# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('judge_interface', '0016_auto_20150914_1849'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='participant',
            name='uuid',
        ),
        migrations.AlterField(
            model_name='participant',
            name='avatar',
            field=models.CharField(default=b'', max_length=250),
        ),
    ]
