# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2022-06-29 14:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polybookexchange', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='cover',
            field=models.ImageField(upload_to='poylbookexchange/covers'),
        ),
    ]
