# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-12 06:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OnlineLibraryApp', '0008_auto_20160512_1423'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='attime',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
