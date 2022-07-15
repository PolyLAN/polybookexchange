from django import template
from polybookexchange.models import Exemplar
from django.db.models import Avg, Sum

register = template.Library()

from polybookexchange.utils import sciper2name


@register.inclusion_tag("polybookexchange/templatetags/show_book.html")
def show_book(book, show_details):

    return {"book": book, "show_details": show_details == "True"}


@register.inclusion_tag("polybookexchange/templatetags/show_small_book.html")
def show_small_book(book):

    return {"book": book}


@register.inclusion_tag("polybookexchange/templatetags/show_for_sem_sec.html")
def show_for_sem_sec(book, sem, sec):

    return {"val": book.usedby_set.filter(section=sec).filter(semester=sem).count() > 0}


@register.inclusion_tag("polybookexchange/templatetags/checked.html")
def checked_case(book, sem, sec, candi):

    val = book.usedby_set.filter(section=sec).filter(semester=sem).count()

    if candi:
        val = val or candi.candidateusage_set.filter(section=sec).filter(semester=sem).count()

    return {"val": val}


@register.inclusion_tag("polybookexchange/templatetags/stats.html")
def show_stats():
    v = Exemplar.objects.aggregate(Avg("price"), Sum("price"))

    return {
        "nb_exemplaires": Exemplar.objects.filter(sold_date=None).count(),
        "nb_exemplaires_vendu": Exemplar.objects.exclude(sold_date=None).count(),
        "total": v["price__sum"],
        "average": v["price__avg"],
    }


@register.inclusion_tag("polybookexchange/templatetags/show_name_from_sciper.html")
def show_name_from_sciper(sciper):

    name = sciper2name(sciper)

    return {"sciper": sciper, "name": name}
