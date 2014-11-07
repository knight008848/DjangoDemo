# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='changelog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('action_time', models.DateTimeField()),
                ('message', models.TextField(max_length=200)),
                ('action_status', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='platform',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=45)),
                ('model', models.CharField(max_length=45)),
                ('lob', models.CharField(max_length=45)),
                ('type', models.CharField(max_length=45)),
                ('pebit', models.CharField(max_length=45)),
                ('product', models.CharField(max_length=45)),
                ('phnum', models.CharField(max_length=45, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
