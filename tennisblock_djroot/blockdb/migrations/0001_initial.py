# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Season'
        db.create_table(u'blockdb_season', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('courts', self.gf('django.db.models.fields.IntegerField')()),
            ('firstcourt', self.gf('django.db.models.fields.IntegerField')()),
            ('startdate', self.gf('django.db.models.fields.DateField')()),
            ('enddate', self.gf('django.db.models.fields.DateField')()),
            ('blockstart', self.gf('django.db.models.fields.DateField')()),
            ('blocktime', self.gf('django.db.models.fields.TimeField')()),
        ))
        db.send_create_signal(u'blockdb', ['Season'])

        # Adding model 'Player'
        db.create_table(u'blockdb_player', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('last', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('ntrp', self.gf('django.db.models.fields.FloatField')()),
            ('microntrp', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=14, blank=True)),
        ))
        db.send_create_signal(u'blockdb', ['Player'])

        # Adding model 'Couple'
        db.create_table(u'blockdb_couple', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('season', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blockdb.Season'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('male', self.gf('django.db.models.fields.related.ForeignKey')(related_name='guy', to=orm['blockdb.Player'])),
            ('female', self.gf('django.db.models.fields.related.ForeignKey')(related_name='gal', to=orm['blockdb.Player'])),
            ('fulltime', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('canschedule', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('blockcouple', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'blockdb', ['Couple'])

        # Adding model 'Meetings'
        db.create_table(u'blockdb_meetings', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('season', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blockdb.Season'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('holdout', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('comments', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal(u'blockdb', ['Meetings'])

        # Adding model 'Availability'
        db.create_table(u'blockdb_availability', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('meeting', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blockdb.Meetings'])),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blockdb.Player'])),
            ('available', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'blockdb', ['Availability'])

        # Adding model 'SeasonPlayers'
        db.create_table(u'blockdb_seasonplayers', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('season', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blockdb.Season'])),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blockdb.Player'])),
            ('blockmember', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'blockdb', ['SeasonPlayers'])

        # Adding model 'Schedule'
        db.create_table(u'blockdb_schedule', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('meeting', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blockdb.Meetings'])),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blockdb.Player'])),
            ('issub', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('verified', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'blockdb', ['Schedule'])

        # Adding model 'Slot'
        db.create_table(u'blockdb_slot', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('meeting', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blockdb.Meetings'])),
            ('set', self.gf('django.db.models.fields.IntegerField')()),
            ('court', self.gf('django.db.models.fields.IntegerField')()),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blockdb.Player'])),
            ('position', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal(u'blockdb', ['Slot'])

        # Adding model 'Team'
        db.create_table(u'blockdb_team', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('male', self.gf('django.db.models.fields.related.ForeignKey')(related_name='team_guy', to=orm['blockdb.Player'])),
            ('female', self.gf('django.db.models.fields.related.ForeignKey')(related_name='team_gal', to=orm['blockdb.Player'])),
        ))
        db.send_create_signal(u'blockdb', ['Team'])

        # Adding model 'Matchup'
        db.create_table(u'blockdb_matchup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('meeting', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blockdb.Meetings'])),
            ('set', self.gf('django.db.models.fields.IntegerField')()),
            ('court', self.gf('django.db.models.fields.IntegerField')()),
            ('team1', self.gf('django.db.models.fields.related.ForeignKey')(related_name='team1', to=orm['blockdb.Team'])),
            ('team2', self.gf('django.db.models.fields.related.ForeignKey')(related_name='team2', to=orm['blockdb.Team'])),
        ))
        db.send_create_signal(u'blockdb', ['Matchup'])


    def backwards(self, orm):
        # Deleting model 'Season'
        db.delete_table(u'blockdb_season')

        # Deleting model 'Player'
        db.delete_table(u'blockdb_player')

        # Deleting model 'Couple'
        db.delete_table(u'blockdb_couple')

        # Deleting model 'Meetings'
        db.delete_table(u'blockdb_meetings')

        # Deleting model 'Availability'
        db.delete_table(u'blockdb_availability')

        # Deleting model 'SeasonPlayers'
        db.delete_table(u'blockdb_seasonplayers')

        # Deleting model 'Schedule'
        db.delete_table(u'blockdb_schedule')

        # Deleting model 'Slot'
        db.delete_table(u'blockdb_slot')

        # Deleting model 'Team'
        db.delete_table(u'blockdb_team')

        # Deleting model 'Matchup'
        db.delete_table(u'blockdb_matchup')


    models = {
        u'blockdb.availability': {
            'Meta': {'object_name': 'Availability'},
            'available': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meeting': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['blockdb.Meetings']"}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['blockdb.Player']"})
        },
        u'blockdb.couple': {
            'Meta': {'object_name': 'Couple'},
            'blockcouple': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'canschedule': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'female': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'gal'", 'to': u"orm['blockdb.Player']"}),
            'fulltime': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'male': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'guy'", 'to': u"orm['blockdb.Player']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['blockdb.Season']"})
        },
        u'blockdb.matchup': {
            'Meta': {'object_name': 'Matchup'},
            'court': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meeting': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['blockdb.Meetings']"}),
            'set': ('django.db.models.fields.IntegerField', [], {}),
            'team1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'team1'", 'to': u"orm['blockdb.Team']"}),
            'team2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'team2'", 'to': u"orm['blockdb.Team']"})
        },
        u'blockdb.meetings': {
            'Meta': {'object_name': 'Meetings'},
            'comments': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'holdout': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['blockdb.Season']"})
        },
        u'blockdb.player': {
            'Meta': {'object_name': 'Player'},
            'email': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'first': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'microntrp': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'ntrp': ('django.db.models.fields.FloatField', [], {}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '14', 'blank': 'True'})
        },
        u'blockdb.schedule': {
            'Meta': {'object_name': 'Schedule'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issub': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'meeting': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['blockdb.Meetings']"}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['blockdb.Player']"}),
            'verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'blockdb.season': {
            'Meta': {'object_name': 'Season'},
            'blockstart': ('django.db.models.fields.DateField', [], {}),
            'blocktime': ('django.db.models.fields.TimeField', [], {}),
            'courts': ('django.db.models.fields.IntegerField', [], {}),
            'enddate': ('django.db.models.fields.DateField', [], {}),
            'firstcourt': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'startdate': ('django.db.models.fields.DateField', [], {})
        },
        u'blockdb.seasonplayers': {
            'Meta': {'object_name': 'SeasonPlayers'},
            'blockmember': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['blockdb.Player']"}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['blockdb.Season']"})
        },
        u'blockdb.slot': {
            'Meta': {'object_name': 'Slot'},
            'court': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meeting': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['blockdb.Meetings']"}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['blockdb.Player']"}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'set': ('django.db.models.fields.IntegerField', [], {})
        },
        u'blockdb.team': {
            'Meta': {'object_name': 'Team'},
            'female': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'team_gal'", 'to': u"orm['blockdb.Player']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'male': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'team_guy'", 'to': u"orm['blockdb.Player']"})
        }
    }

    complete_apps = ['blockdb']