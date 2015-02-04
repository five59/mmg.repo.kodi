# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20150204_0022'),
    ]

    operations = [
        migrations.AddField(
            model_name='streamtype',
            name='token',
            field=models.IntegerField(default=30000, max_length=5),
            preserve_default=False,
        ),
    ]
