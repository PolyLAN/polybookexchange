# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('isbn', models.DecimalField(serialize=False, primary_key=True, decimal_places=0, max_digits=13)),
                ('title', models.CharField(max_length=255)),
                ('original_title', models.CharField(max_length=255)),
                ('edition', models.PositiveSmallIntegerField()),
                ('year', models.PositiveIntegerField()),
                ('avg_price', models.FloatField(default=0, null=True, blank=True)),
                ('qty_in_stock', models.IntegerField(default=0)),
                ('qty_sold', models.IntegerField(default=0)),
                ('cover', models.ImageField(upload_to=b'poylbookexchange/covers')),
                ('author', models.ManyToManyField(to='polybookexchange.Author')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('isbn', models.DecimalField(max_digits=13, decimal_places=0)),
                ('sciper', models.PositiveIntegerField()),
                ('annotated', models.BooleanField(default=False)),
                ('highlighted', models.BooleanField(default=False)),
                ('state', models.CharField(max_length=10, choices=[('neuf', 'neuf'), ('bon', 'bon'), ('acceptable', 'acceptable'), ('mauvais', 'mauvais')])),
                ('comments', models.TextField()),
                ('price', models.FloatField()),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CandidateUsage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('candidate', models.ForeignKey(to='polybookexchange.Candidate')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Exemplar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.FloatField()),
                ('seller_id', models.PositiveIntegerField()),
                ('buyer_id', models.PositiveIntegerField(null=True, blank=True)),
                ('posted_date', models.DateTimeField(auto_now_add=True)),
                ('sold_date', models.DateTimeField(null=True, blank=True)),
                ('out_reason', models.CharField(max_length=50, null=True, choices=[('sold', 'Vendu'), ('expired', 'Donn\xe9 \xe0 la biblioth\xe8que centrale'), ('retrieved', 'Rendu \xe0 son propri\xe9taire'), ('lost', 'Perdu')])),
                ('money_given_date', models.DateTimeField(null=True, blank=True)),
                ('annotated', models.BooleanField(default=False)),
                ('highlighted', models.BooleanField(default=False)),
                ('state', models.CharField(max_length=10, choices=[('neuf', 'neuf'), ('bon', 'bon'), ('acceptable', 'acceptable'), ('mauvais', 'mauvais')])),
                ('comments', models.TextField(null=True, blank=True)),
                ('book', models.ForeignKey(to='polybookexchange.Book')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('acronym', models.CharField(max_length=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('acronym', models.CharField(max_length=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UsedBy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('book', models.ForeignKey(to='polybookexchange.Book')),
                ('section', models.ForeignKey(to='polybookexchange.Section')),
                ('semester', models.ForeignKey(to='polybookexchange.Semester')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='candidateusage',
            name='section',
            field=models.ForeignKey(to='polybookexchange.Section'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='candidateusage',
            name='semester',
            field=models.ForeignKey(to='polybookexchange.Semester'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='book',
            name='publisher',
            field=models.ForeignKey(to='polybookexchange.Publisher'),
            preserve_default=True,
        ),
    ]
