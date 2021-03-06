# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-30 09:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HttpProxyInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('IP', models.GenericIPAddressField(verbose_name='HTTP代理地址')),
                ('ISP', models.CharField(max_length=32, verbose_name='ISP')),
                ('ExpireTime', models.CharField(max_length=32, verbose_name='过期时间')),
                ('IpAddress', models.CharField(max_length=32, verbose_name='归属地')),
            ],
        ),
    ]
