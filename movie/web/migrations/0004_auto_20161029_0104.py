# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-28 17:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_auto_20161028_2316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actor',
            name='avatar',
            field=models.ImageField(help_text='\u5934\u50cf', max_length=200, upload_to='img/avatar/'),
        ),
    ]
