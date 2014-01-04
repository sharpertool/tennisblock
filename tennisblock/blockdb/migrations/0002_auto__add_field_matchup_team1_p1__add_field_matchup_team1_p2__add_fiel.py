# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Matchup.team1_p1'
        db.add_column(u'blockdb_matchup', 'team1_p1',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='t1_p1', null=True, to=orm['blockdb.Player']),
                      keep_default=False)

        # Adding field 'Matchup.team1_p2'
        db.add_column(u'blockdb_matchup', 'team1_p2',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='t1_p2', null=True, to=orm['blockdb.Player']),
                      keep_default=False)

        # Adding field 'Matchup.team2_p1'
        db.add_column(u'blockdb_matchup', 'team2_p1',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='t2_p1', null=True, to=orm['blockdb.Player']),
                      keep_default=False)

        # Adding field 'Matchup.team2_p2'
        db.add_column(u'blockdb_matchup', 'team2_p2',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='t2_p2', null=True, to=orm['blockdb.Player']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Matchup.team1_p1'
        db.delete_column(u'blockdb_matchup', 'team1_p1_id')

        # Deleting field 'Matchup.team1_p2'
        db.delete_column(u'blockdb_matchup', 'team1_p2_id')

        # Deleting field 'Matchup.team2_p1'
        db.delete_column(u'blockdb_matchup', 'team2_p1_id')

        # Deleting field 'Matchup.team2_p2'
        db.delete_column(u'blockdb_matchup', 'team2_p2_id')


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
            'team1_p1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'t1_p1'", 'null': 'True', 'to': u"orm['blockdb.Player']"}),
            'team1_p2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'t1_p2'", 'null': 'True', 'to': u"orm['blockdb.Player']"}),
            'team2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'team2'", 'to': u"orm['blockdb.Team']"}),
            'team2_p1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'t2_p1'", 'null': 'True', 'to': u"orm['blockdb.Player']"}),
            'team2_p2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'t2_p2'", 'null': 'True', 'to': u"orm['blockdb.Player']"})
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
            'partner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'partner'", 'null': 'True', 'to': u"orm['blockdb.Player']"}),
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