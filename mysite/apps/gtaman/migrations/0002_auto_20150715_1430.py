# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gtaman', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gcfnote',
            name='siaccount',
            field=models.CharField(max_length=45, null=True, blank=True),
            preserve_default=True,
        ),
    ]
