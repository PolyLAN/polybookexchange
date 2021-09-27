# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url


urlpatterns = patterns('polybookexchange.views',
    url(r'^$', 'home'),
    url(r'^howTo$', 'howto'),
    url(r'^book/(?P<isbn>[0-9]*)$', 'book'),
    url(r'^exemplar/(?P<id>[0-9]*)$', 'exemplar'),
    url(r'^browse$', 'browse'),
    url(r'^search$', 'search'),
    url(r'^purchases$', 'purchases'),
    url(r'^sales$', 'sales'),
    url(r'^change_price/(?P<id>[0-9]+)$', 'change_price'),
    url(r'^proposed$', 'proposed'),
    url(r'^candidate_card/(?P<id>[0-9]+)$', 'candidate_card'),
    url(r'^propose$', 'propose'),
    url(r'^check_isbn$', 'check_isbn'),
    url(r'^admin$', 'admin'),
    url(r'^admin/sell$', 'sell_book'),
    url(r'^admin/remove$', 'remove_book'),
    url(r'^admin/list_candidates$', 'list_candidates'),
    url(r'^admin/transactions$', 'transactions'),
    url(r'^admin/clean_candidates$', 'clean_candidates'),
    url(r'^admin/edit_book/(?P<isbn>[0-9]+)$', 'edit_book'),
    url(r'^admin/add_book$', 'add_book'),
    url(r'^admin/add_exemplar$', 'add_exemplar'),
    url(r'^admin/exemplar_print/(?P<id>[0-9]*)$', 'exemplar_print'),
    url(r'^gen_bar_code/(?P<code>[0-9]+)$', 'gen_bar_code'),
)
