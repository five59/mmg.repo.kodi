# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='appmeta',
            options={'verbose_name': 'App Metadata', 'verbose_name_plural': 'App Metadata'},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='channel',
            options={'verbose_name': 'Channel', 'verbose_name_plural': 'Channels'},
        ),
        migrations.AlterModelOptions(
            name='streamtype',
            options={'verbose_name': 'Stream Type', 'verbose_name_plural': 'Stream Types'},
        ),
    ]
