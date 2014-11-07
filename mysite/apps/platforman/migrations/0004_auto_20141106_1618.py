# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('platforman', '0003_delete_changelog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='platform',
            name='phnum',
            field=models.CharField(max_length=45, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='platform',
            name='product',
            field=models.CharField(max_length=80, null=True, blank=True),
        ),
    ]
