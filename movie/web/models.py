# coding=utf-8
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Actor(models.Model):
    name = models.CharField(max_length=20, help_text="姓名")
    introduce = models.TextField(help_text="简介")
    avatar = models.ImageField(max_length=200, help_text="头像", upload_to='img/avatar/')
    baidu_url = models.URLField(max_length=200, help_text="百度百科地址", unique=True)