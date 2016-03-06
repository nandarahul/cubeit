# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-21 11:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cubeapp', '0002_auto_20160220_0814'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cubecontent',
            name='content',
        ),
        migrations.RemoveField(
            model_name='cubecontent',
            name='cube',
        ),
        migrations.RemoveField(
            model_name='content',
            name='user',
        ),
        migrations.RemoveField(
            model_name='cube',
            name='user',
        ),
        migrations.AddField(
            model_name='content',
            name='users',
            field=models.ManyToManyField(to='cubeapp.User'),
        ),
        migrations.AddField(
            model_name='cube',
            name='contents',
            field=models.ManyToManyField(to='cubeapp.Content'),
        ),
        migrations.AddField(
            model_name='cube',
            name='users',
            field=models.ManyToManyField(to='cubeapp.User'),
        ),
        migrations.DeleteModel(
            name='CubeContent',
        ),
    ]