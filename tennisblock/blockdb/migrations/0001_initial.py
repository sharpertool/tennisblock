# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Availability',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('available', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Couple',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('fulltime', models.BooleanField(default=False)),
                ('canschedule', models.BooleanField(default=False)),
                ('blockcouple', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Matchup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('set', models.IntegerField()),
                ('court', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Meetings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('holdout', models.BooleanField(default=False)),
                ('comments', models.CharField(max_length=128)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first', models.CharField(max_length=40)),
                ('last', models.CharField(max_length=60)),
                ('gender', models.CharField(max_length=1, choices=[('F', 'Gal'), ('M', 'Guy')])),
                ('ntrp', models.FloatField()),
                ('microntrp', models.FloatField(null=True, blank=True)),
                ('email', models.CharField(max_length=50, blank=True)),
                ('phone', models.CharField(max_length=14, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('issub', models.BooleanField(default=False)),
                ('verified', models.BooleanField(default=False)),
                ('meeting', models.ForeignKey(to='blockdb.Meetings', on_delete=models.CASCADE)),
                ('partner', models.ForeignKey(related_name='partner', to='blockdb.Player', null=True, on_delete=models.CASCADE)),
                ('player', models.ForeignKey(to='blockdb.Player', on_delete=models.CASCADE)),
            ],
            options={
                'permissions': (('change_sched', 'Can change the schedule'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('courts', models.IntegerField()),
                ('firstcourt', models.IntegerField()),
                ('startdate', models.DateField()),
                ('enddate', models.DateField()),
                ('blockstart', models.DateField()),
                ('blocktime', models.TimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SeasonPlayers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('blockmember', models.BooleanField(default=False)),
                ('player', models.ForeignKey(to='blockdb.Player', on_delete=models.CASCADE)),
                ('season', models.ForeignKey(to='blockdb.Season', on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='meetings',
            name='season',
            field=models.ForeignKey(to='blockdb.Season', on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='matchup',
            name='meeting',
            field=models.ForeignKey(to='blockdb.Meetings', on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='matchup',
            name='team1_p1',
            field=models.ForeignKey(related_name='t1_p1', to='blockdb.Player', null=True, on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='matchup',
            name='team1_p2',
            field=models.ForeignKey(related_name='t1_p2', to='blockdb.Player', null=True, on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='matchup',
            name='team2_p1',
            field=models.ForeignKey(related_name='t2_p1', to='blockdb.Player', null=True, on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='matchup',
            name='team2_p2',
            field=models.ForeignKey(related_name='t2_p2', to='blockdb.Player', null=True, on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='couple',
            name='female',
            field=models.ForeignKey(related_name='gal', to='blockdb.Player', on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='couple',
            name='male',
            field=models.ForeignKey(related_name='guy', to='blockdb.Player', on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='couple',
            name='season',
            field=models.ForeignKey(to='blockdb.Season', on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='availability',
            name='meeting',
            field=models.ForeignKey(to='blockdb.Meetings', on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='availability',
            name='player',
            field=models.ForeignKey(to='blockdb.Player', on_delete=models.CASCADE),
            preserve_default=True,
        ),
    ]
