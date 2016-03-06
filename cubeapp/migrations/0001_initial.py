# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-17 22:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Cube',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='cube',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cubeapp.User'),
        ),
        migrations.AddField(
            model_name='content',
            name='cube',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cubeapp.Cube'),
        ),
        migrations.AddField(
            model_name='content',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cubeapp.User'),
        ),
    ]
