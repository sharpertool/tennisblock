# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Team'
        db.delete_table(u'blockdb_team')

        # Deleting field 'Matchup.team1'
        db.delete_column(u'blockdb_matchup', 'team1_id')

        # Deleting field 'Matchup.team2'
        db.delete_column(u'blockdb_matchup', 'team2_id')


    def backwards(self, orm):
        # Adding model 'Team'
        db.create_table(u'blockdb_team', (
            ('male', self.gf('django.db.models.fields.related.ForeignKey')(related_name='team_guy', to=orm['blockdb.Player'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('female', self.gf('django.db.models.fields.related.ForeignKey')(related_name='team_gal', to=orm['blockdb.Player'])),
        ))
        db.send_create_signal(u'blockdb', ['Team'])

        # Adding field 'Matchup.team1'
        db.add_column(u'blockdb_matchup', 'team1',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, related_name='team1', to=orm['blockdb.Team']),
                      keep_default=False)

        # Adding field 'Matchup.team2'
        db.add_column(u'blockdb_matchup', 'team2',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, related_name='team2', to=orm['blockdb.Team']),
                      keep_default=False)


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
            'team1_p1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'t1_p1'", 'null': 'True', 'to': u"orm['blockdb.Player']"}),
            'team1_p2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'t1_p2'", 'null': 'True', 'to': u"orm['blockdb.Player']"}),
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
        }
    }

    complete_apps = ['blockdb']