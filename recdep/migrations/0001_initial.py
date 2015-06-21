# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('addr', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ProbeReq',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField()),
                ('node', models.ForeignKey(to='recdep.Node')),
            ],
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ServiceSet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ssid', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='SignalStrength',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_recorded', models.DateTimeField()),
                ('rssi', models.IntegerField(help_text=b'Received signal strength')),
                ('iee80211_frame_sha256_hash', models.CharField(help_text=b'The hash over the IEEE8 802.11 that has been received.', max_length=64)),
            ],
        ),
        migrations.AddField(
            model_name='probereq',
            name='sensor',
            field=models.ForeignKey(to='recdep.Sensor'),
        ),
        migrations.AddField(
            model_name='probereq',
            name='serviceset',
            field=models.ForeignKey(to='recdep.ServiceSet'),
        ),
    ]
