# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-12 10:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OnlineLibraryApp', '0009_auto_20160512_1427'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='imageurl',
            field=models.CharField(default=b'http://www.readanybook.com/covers/105799/small', max_length=200),
        ),
    ]
