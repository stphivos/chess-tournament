# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('judge_interface', '0013_auto_20150914_1223'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='avatar',
            field=models.ImageField(null=True, upload_to=b'/media/'),
        ),
    ]
