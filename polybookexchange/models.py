# -*- coding: UTF-8 -*-

from django.db import models
from django.db.models import Min
import requests
import isbnlib
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.templatetags.static import static
from django.conf import settings
import datetime
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


class Book(models.Model):

    isbn = models.DecimalField(primary_key=True, max_digits=13, decimal_places=0)
    title = models.CharField(max_length=255)
    original_title = models.CharField(max_length=255)
    edition = models.PositiveSmallIntegerField()
    year = models.PositiveIntegerField()
    avg_price = models.FloatField(default=0, blank=True, null=True)
    qty_in_stock = models.IntegerField(default=0)
    qty_sold = models.IntegerField(default=0)
    publisher = models.ForeignKey('Publisher', on_delete=models.CASCADE)
    author = models.ManyToManyField('Author')
    cover = models.ImageField(upload_to='poylbookexchange/covers')

    def sellable(self):
        return self.exemplar_set.filter(buyer_id=None).order_by('pk').all()

    def sold(self):
        return self.exemplar_set.exclude(buyer_id=None).order_by('pk').all()

    def used_in_sections(self):
        return Section.objects.filter(usedby__book__pk=self.pk).distinct().order_by('pk').all()

    def used_in_semesters(self):
        return Semester.objects.filter(usedby__book__pk=self.pk).distinct().order_by('pk').all()

    def update_metadata(self):

        try:
            data = isbnlib.meta(str(self.isbn), 'wcat')

            self.title = data.get('Title')
            self.year = data.get('Year') or 1900
            self.publisher, _ = Publisher.objects.get_or_create(name=data.get('Publisher', 'Unknow'))
            self.author.clear()

            for author in data.get('Authors', []):
                for splited_author in author.split(', '):
                    author_object, _ = Author.objects.get_or_create(name=splited_author)

                    self.author.add(author_object)
        except:

            self.title = self.title or '?'
            self.year = self.year or 1900

            try:
                truc = self.publisher
            except:
                self.publisher, _ = Publisher.objects.get_or_create(name='Unknow')

        self.save()

    def update_cover(self):

        image = requests.get('http://images.amazon.com/images/P/%s.01._SS500_SCLZZZZZZZ_.jpg' % (isbnlib.to_isbn10(str(self.isbn)), ))

        if image.status_code == 200 and len(image.content) > 50:
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(image.content)
            img_temp.flush()

            self.cover.save('%s.jpg' % (self.isbn,), File(img_temp))

        else:
            self.cover.delete()

    def get_current_cover(self):
        if self.cover:
            return settings.MEDIA_URL + self.cover.name

        return static('polybookexchange/default.png')


class Candidate(models.Model):

    STATE_CHOICES = (
        ('neuf', _('neuf')),
        ('bon', _('bon')),
        ('acceptable', _('acceptable')),
        ('mauvais', _('mauvais')),
    )

    isbn = models.DecimalField(max_digits=13, decimal_places=0)
    sciper = models.PositiveIntegerField()
    annotated = models.BooleanField(default=False)
    highlighted = models.BooleanField(default=False)
    state = models.CharField(max_length=10, choices=STATE_CHOICES)
    comments = models.TextField()
    price = models.FloatField()
    creation_date = models.DateTimeField(auto_now_add=True)

    def days_left(self):
        diff = (self.creation_date + datetime.timedelta(days=16) - now()).days

        if diff < 0:
            diff = 0

        return diff

    def days_left_percent(self):
        return int(((15 - self.days_left()) * 100.0) / 15.0)

    def days_left_color(self):

        if self.days_left() < 1:
            return 'danger'
        if self.days_left() < 5:
            return 'warning'

        return 'success'


class CandidateUsage(models.Model):

    candidate = models.ForeignKey('Candidate', on_delete=models.CASCADE)
    section = models.ForeignKey('Section', on_delete=models.CASCADE)
    semester = models.ForeignKey('Semester', on_delete=models.CASCADE)


class Exemplar(models.Model):

    STATE_CHOICES = (
        ('neuf', _('neuf')),
        ('bon', _('bon')),
        ('acceptable', _('acceptable')),
        ('mauvais', _('mauvais')),
    )

    OUT_REASON_CHOICES = (
        ('sold', _('Vendu')),
        ('expired', _('Donné à la bibliothèque centrale')),  # given to EPFL library
        ('retrieved', _('Rendu à son propriétaire')),  # user got it back
        ('lost', _('Perdu')),
    )

    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    price = models.FloatField()
    seller_id = models.PositiveIntegerField()
    buyer_id = models.PositiveIntegerField(null=True, blank=True)
    posted_date = models.DateTimeField(auto_now_add=True)
    sold_date = models.DateTimeField(null=True, blank=True)
    out_reason = models.CharField(null=True, max_length=50, choices=OUT_REASON_CHOICES)
    money_given_date = models.DateTimeField(null=True, blank=True)
    annotated = models.BooleanField(default=False)
    highlighted = models.BooleanField(default=False)
    state = models.CharField(max_length=10, choices=STATE_CHOICES)
    comments = models.TextField(blank=True, null=True)

    def min_price(self):
        return Exemplar.objects.filter(book=self.book).exclude(sold_date=None).aggregate(Min('price'))['price__min']

    def state_color(self):
        mapping = {
            'neuf': 'success',
            'bon': 'info',
            'acceptable': 'warning',
            'mauvais': 'danger'
        }

        return mapping.get(self.state, 'primary')


class Publisher(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Section(models.Model):
    name = models.CharField(max_length=255)
    acronym = models.CharField(max_length=10)


class Semester(models.Model):
    name = models.CharField(max_length=255)
    acronym = models.CharField(max_length=10)


class UsedBy(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    section = models.ForeignKey('Section', on_delete=models.CASCADE)
    semester = models.ForeignKey('Semester', on_delete=models.CASCADE)
