# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('judge_interface', '0015_auto_20150914_1800'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='uuid',
            field=models.CharField(default=uuid.uuid4, max_length=50, blank=True),
        ),
        migrations.AlterField(
            model_name='participant',
            name='avatar',
            field=models.ImageField(null=True, upload_to=b'media', blank=True),
        ),
    ]
