# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gtaman', '0002_auto_20150715_1430'),
    ]

    operations = [
        migrations.AddField(
            model_name='gcfnote',
            name='cfiflag',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gcfnote',
            name='muiflag',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
