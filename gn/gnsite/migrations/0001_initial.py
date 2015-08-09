# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('dt_created', models.DateTimeField(auto_now_add=True)),
                ('dt_modified', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=200)),
                ('desc', models.TextField(blank=True, max_length=1000)),
                ('link', models.URLField(blank=True, max_length=1000)),
                ('op', models.ForeignKey(related_name='posts', to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(to='gnsite.Post', blank=True, null=True, related_name='comments')),
                ('votes', models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='votes')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
