# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_streamtype_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='streamtype',
            name='token',
        ),
        migrations.AddField(
            model_name='category',
            name='token',
            field=models.IntegerField(default=30000, max_length=5),
            preserve_default=False,
        ),
    ]
