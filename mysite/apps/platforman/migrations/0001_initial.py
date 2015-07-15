# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='platform',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=45)),
                ('model', models.CharField(max_length=45)),
                ('lob', models.CharField(max_length=45)),
                ('type', models.CharField(max_length=45)),
                ('pebit', models.CharField(max_length=45)),
                ('product', models.CharField(max_length=80, null=True, blank=True)),
                ('phnum', models.CharField(max_length=45, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
