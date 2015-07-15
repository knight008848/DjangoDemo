# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='gcfnote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('po', models.CharField(unique=True, max_length=45)),
                ('timestamp', models.DateTimeField()),
                ('model', models.CharField(max_length=45)),
                ('family', models.CharField(max_length=45)),
                ('level', models.CharField(max_length=45)),
                ('region', models.CharField(max_length=45)),
                ('ctomod', models.CharField(max_length=45)),
                ('destination', models.CharField(max_length=45)),
                ('OSP', models.CharField(max_length=45)),
                ('OSD', models.CharField(max_length=45)),
                ('siaccount', models.CharField(max_length=80, null=True, blank=True)),
                ('mod', models.TextField()),
                ('sdr', models.TextField()),
                ('filepath', models.CharField(max_length=80)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
