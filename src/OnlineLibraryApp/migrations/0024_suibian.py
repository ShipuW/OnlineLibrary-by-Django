# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-20 09:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OnlineLibraryApp', '0023_auto_20160514_2102'),
    ]

    operations = [
        migrations.CreateModel(
            name='SuiBian',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=b'shipu', max_length=50)),
            ],
            options={
                'db_table': 'suibian',
            },
        ),
    ]
