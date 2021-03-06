# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-30 10:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GetIpAddress', '0002_httpproxyinfo_used'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgentInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('AgentName', models.CharField(max_length=16, verbose_name='客户端名称')),
                ('AgentIP', models.GenericIPAddressField(verbose_name='客户端地址')),
                ('Key', models.CharField(max_length=32, verbose_name='认证key信息')),
            ],
        ),
    ]
