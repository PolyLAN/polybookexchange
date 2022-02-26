# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Exemplar.out_reason'
        db.add_column(u'polybookexchange_exemplar', 'out_reason',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True),
                      keep_default=False)

        # Adding field 'Exemplar.money_given_date'
        db.add_column(u'polybookexchange_exemplar', 'money_given_date',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)


        # Changing field 'Exemplar.comments'
        db.alter_column(u'polybookexchange_exemplar', 'comments', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Book.avg_price'
        db.alter_column(u'polybookexchange_book', 'avg_price', self.gf('django.db.models.fields.FloatField')(null=True))

    def backwards(self, orm):
        # Deleting field 'Exemplar.out_reason'
        db.delete_column(u'polybookexchange_exemplar', 'out_reason')

        # Deleting field 'Exemplar.money_given_date'
        db.delete_column(u'polybookexchange_exemplar', 'money_given_date')


        # Changing field 'Exemplar.comments'
        db.alter_column(u'polybookexchange_exemplar', 'comments', self.gf('django.db.models.fields.TextField')(default=''))

        # Changing field 'Book.avg_price'
        db.alter_column(u'polybookexchange_book', 'avg_price', self.gf('django.db.models.fields.FloatField')(default=0.0))

    models = {
        u'polybookexchange.author': {
            'Meta': {'object_name': 'Author'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'polybookexchange.book': {
            'Meta': {'object_name': 'Book'},
            'author': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['polybookexchange.Author']", 'symmetrical': 'False'}),
            'avg_price': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'cover': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'edition': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'isbn': ('django.db.models.fields.DecimalField', [], {'primary_key': 'True', 'decimal_places': '0', 'max_digits': '13'}),
            'original_title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'publisher': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['polybookexchange.Publisher']"}),
            'qty_in_stock': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'qty_sold': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'year': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'polybookexchange.candidate': {
            'Meta': {'object_name': 'Candidate'},
            'annotated': ('django.db.models.fields.BooleanField', [], {}),
            'comments': ('django.db.models.fields.TextField', [], {}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'highlighted': ('django.db.models.fields.BooleanField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isbn': ('django.db.models.fields.DecimalField', [], {'max_digits': '13', 'decimal_places': '0'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'sciper': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'polybookexchange.candidateusage': {
            'Meta': {'object_name': 'CandidateUsage'},
            'candidate': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['polybookexchange.Candidate']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['polybookexchange.Section']"}),
            'semester': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['polybookexchange.Semester']"})
        },
        u'polybookexchange.exemplar': {
            'Meta': {'object_name': 'Exemplar'},
            'annotated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'book': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['polybookexchange.Book']"}),
            'buyer_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'highlighted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'money_given_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'out_reason': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'posted_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'seller_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'sold_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'polybookexchange.publisher': {
            'Meta': {'object_name': 'Publisher'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'polybookexchange.section': {
            'Meta': {'object_name': 'Section'},
            'acronym': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'polybookexchange.semester': {
            'Meta': {'object_name': 'Semester'},
            'acronym': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'polybookexchange.usedby': {
            'Meta': {'object_name': 'UsedBy'},
            'book': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['polybookexchange.Book']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['polybookexchange.Section']"}),
            'semester': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['polybookexchange.Semester']"})
        }
    }

    complete_apps = ['polybookexchange']