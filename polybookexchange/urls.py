# -*- coding: utf-8 -*-

from django.urls import path

from polybookexchange import views


urlpatterns = [
    path('', views.home, name="polybookexchange.views.home"),
    path('howTo', views.howto, name="polybookexchange.views.howto"),
    path('book/<int:isbn>', views.book, name="polybookexchange.views.book"),
    path('exemplar/<int:id>', views.exemplar, name="polybookexchange.views.exemplar"),
    path('browse', views.browse, name="polybookexchange.views.browse"),
    path('search', views.search, name="polybookexchange.views.search"),
    path('purchases', views.purchases, name="polybookexchange.views.purchases"),
    path('sales', views.sales, name="polybookexchange.views.sales"),
    path('change_price/<int:id>', views.change_price, name="polybookexchange.views.change_price"),
    path('proposed', views.proposed, name="polybookexchange.views.proposed"),
    path('candidate_card/<int:id>', views.candidate_card, name="polybookexchange.views.candidate_card"),
    path('propose', views.propose, name="polybookexchange.views.propose"),
    path('check_isbn', views.check_isbn, name="polybookexchange.views.check_isbn"),
    path('admin', views.admin, name="polybookexchange.views.admin"),
    path('admin/sell', views.sell_book, name="polybookexchange.views.sell_book"),
    path('admin/give_money_back', views.give_money_back, name="polybookexchange.views.give_money_back"),
    path('admin/remove', views.remove_book, name="polybookexchange.views.remove_book"),
    path('admin/list_candidates', views.list_candidates, name="polybookexchange.views.list_candidates"),
    path('admin/transactions', views.transactions, name="polybookexchange.views.transactions"),
    path('admin/clean_candidates', views.clean_candidates, name="polybookexchange.views.clean_candidates"),
    path('admin/financial_infos', views.financial_infos, name="polybookexchange.views.financial_infos"),
    path('admin/edit_book/<int:isbn>', views.edit_book, name="polybookexchange.views.edit_book"),
    path('admin/add_book', views.add_book, name="polybookexchange.views.add_book"),
    path('admin/add_exemplar', views.add_exemplar, name="polybookexchange.views.add_exemplar"),
    path('admin/exemplar_print/<int:id>', views.exemplar_print, name="polybookexchange.views.exemplar_print"),
    path('gen_bar_code/<int:code>', views.gen_bar_code, name="polybookexchange.views.gen_bar_code"),
]
