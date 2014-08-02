# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Author'
        db.create_table(u'polybookexchange_author', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'polybookexchange', ['Author'])

        # Adding model 'Book'
        db.create_table(u'polybookexchange_book', (
            ('isbn', self.gf('django.db.models.fields.DecimalField')(primary_key=True, decimal_places=0, max_digits=13)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('original_title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('edition', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('year', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('avg_price', self.gf('django.db.models.fields.FloatField')()),
            ('qty_in_stock', self.gf('django.db.models.fields.IntegerField')()),
            ('qty_sold', self.gf('django.db.models.fields.IntegerField')()),
            ('publisher', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['polybookexchange.Publisher'])),
            ('cover', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal(u'polybookexchange', ['Book'])

        # Adding M2M table for field author on 'Book'
        m2m_table_name = db.shorten_name(u'polybookexchange_book_author')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('book', models.ForeignKey(orm[u'polybookexchange.book'], null=False)),
            ('author', models.ForeignKey(orm[u'polybookexchange.author'], null=False))
        ))
        db.create_unique(m2m_table_name, ['book_id', 'author_id'])

        # Adding model 'Candidate'
        db.create_table(u'polybookexchange_candidate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('isbn', self.gf('django.db.models.fields.DecimalField')(max_digits=13, decimal_places=0)),
            ('sciper', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('annotated', self.gf('django.db.models.fields.BooleanField')()),
            ('highlighted', self.gf('django.db.models.fields.BooleanField')()),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('comments', self.gf('django.db.models.fields.TextField')()),
            ('price', self.gf('django.db.models.fields.FloatField')()),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'polybookexchange', ['Candidate'])

        # Adding model 'CandidateUsage'
        db.create_table(u'polybookexchange_candidateusage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('candidate', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['polybookexchange.Candidate'])),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['polybookexchange.Section'])),
            ('semester', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['polybookexchange.Semester'])),
        ))
        db.send_create_signal(u'polybookexchange', ['CandidateUsage'])

        # Adding model 'Exemplar'
        db.create_table(u'polybookexchange_exemplar', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('book', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['polybookexchange.Book'])),
            ('price', self.gf('django.db.models.fields.FloatField')()),
            ('seller_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('buyer_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('posted_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('sold_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('annotated', self.gf('django.db.models.fields.BooleanField')()),
            ('highlighted', self.gf('django.db.models.fields.BooleanField')()),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('comments', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'polybookexchange', ['Exemplar'])

        # Adding model 'Publisher'
        db.create_table(u'polybookexchange_publisher', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'polybookexchange', ['Publisher'])

        # Adding model 'Section'
        db.create_table(u'polybookexchange_section', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('acronym', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal(u'polybookexchange', ['Section'])

        # Adding model 'Semester'
        db.create_table(u'polybookexchange_semester', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('acronym', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal(u'polybookexchange', ['Semester'])

        # Adding model 'UsedBy'
        db.create_table(u'polybookexchange_usedby', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('book', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['polybookexchange.Book'])),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['polybookexchange.Section'])),
            ('semester', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['polybookexchange.Semester'])),
        ))
        db.send_create_signal(u'polybookexchange', ['UsedBy'])


    def backwards(self, orm):
        # Deleting model 'Author'
        db.delete_table(u'polybookexchange_author')

        # Deleting model 'Book'
        db.delete_table(u'polybookexchange_book')

        # Removing M2M table for field author on 'Book'
        db.delete_table(db.shorten_name(u'polybookexchange_book_author'))

        # Deleting model 'Candidate'
        db.delete_table(u'polybookexchange_candidate')

        # Deleting model 'CandidateUsage'
        db.delete_table(u'polybookexchange_candidateusage')

        # Deleting model 'Exemplar'
        db.delete_table(u'polybookexchange_exemplar')

        # Deleting model 'Publisher'
        db.delete_table(u'polybookexchange_publisher')

        # Deleting model 'Section'
        db.delete_table(u'polybookexchange_section')

        # Deleting model 'Semester'
        db.delete_table(u'polybookexchange_semester')

        # Deleting model 'UsedBy'
        db.delete_table(u'polybookexchange_usedby')


    models = {
        u'polybookexchange.author': {
            'Meta': {'object_name': 'Author'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'polybookexchange.book': {
            'Meta': {'object_name': 'Book'},
            'author': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['polybookexchange.Author']", 'symmetrical': 'False'}),
            'avg_price': ('django.db.models.fields.FloatField', [], {}),
            'cover': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'edition': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'isbn': ('django.db.models.fields.DecimalField', [], {'primary_key': 'True', 'decimal_places': '0', 'max_digits': '13'}),
            'original_title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'publisher': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['polybookexchange.Publisher']"}),
            'qty_in_stock': ('django.db.models.fields.IntegerField', [], {}),
            'qty_sold': ('django.db.models.fields.IntegerField', [], {}),
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
            'annotated': ('django.db.models.fields.BooleanField', [], {}),
            'book': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['polybookexchange.Book']"}),
            'buyer_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {}),
            'highlighted': ('django.db.models.fields.BooleanField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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