# -*- coding: utf-8 -*-

from django.conf.urls import url

from polybookexchange import views


urlpatterns = [
    url(r'^$', views.home, name="polybookexchange.views.home"),
    url(r'^howTo$', views.howto, name="polybookexchange.views.howto"),
    url(r'^book/(?P<isbn>[0-9]*)$', views.book, name="polybookexchange.views.book"),
    url(r'^exemplar/(?P<id>[0-9]*)$', views.exemplar, name="polybookexchange.views.exemplar"),
    url(r'^browse$', views.browse, name="polybookexchange.views.browse"),
    url(r'^search$', views.search, name="polybookexchange.views.search"),
    url(r'^purchases$', views.purchases, name="polybookexchange.views.purchases"),
    url(r'^sales$', views.sales, name="polybookexchange.views.sales"),
    url(r'^change_price/(?P<id>[0-9]+)$', views.change_price, name="polybookexchange.views.change_price"),
    url(r'^proposed$', views.proposed, name="polybookexchange.views.proposed"),
    url(r'^candidate_card/(?P<id>[0-9]+)$', views.candidate_card, name="polybookexchange.views.candidate_card"),
    url(r'^propose$', views.propose, name="polybookexchange.views.propose"),
    url(r'^check_isbn$', views.check_isbn, name="polybookexchange.views.check_isbn"),
    url(r'^admin$', views.admin, name="polybookexchange.views.admin"),
    url(r'^admin/sell$', views.sell_book, name="polybookexchange.views.sell_book"),
    url(r'^admin/give_money_back$', views.give_money_back, name="polybookexchange.views.give_money_back"),
    url(r'^admin/remove$', views.remove_book, name="polybookexchange.views.remove_book"),
    url(r'^admin/list_candidates$', views.list_candidates, name="polybookexchange.views.list_candidates"),
    url(r'^admin/transactions$', views.transactions, name="polybookexchange.views.transactions"),
    url(r'^admin/clean_candidates$', views.clean_candidates, name="polybookexchange.views.clean_candidates"),
    url(r'^admin/financial_infos$', views.financial_infos, name="polybookexchange.views.financial_infos"),
    url(r'^admin/edit_book/(?P<isbn>[0-9]+)$', views.edit_book, name="polybookexchange.views.edit_book"),
    url(r'^admin/add_book$', views.add_book, name="polybookexchange.views.add_book"),
    url(r'^admin/add_exemplar$', views.add_exemplar, name="polybookexchange.views.add_exemplar"),
    url(r'^admin/exemplar_print/(?P<id>[0-9]*)$', views.exemplar_print, name="polybookexchange.views.exemplar_print"),
    url(r'^gen_bar_code/(?P<code>[0-9]+)$', views.gen_bar_code, name="polybookexchange.views.gen_bar_code"),
]
