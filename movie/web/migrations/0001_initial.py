# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-28 14:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='\u59d3\u540d', max_length=20)),
                ('introduce', models.TextField(help_text='\u7b80\u4ecb')),
            ],
        ),
    ]
