# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.conf import settings
from .models import Book, Exemplar, Section, Semester, Candidate, CandidateUsage, Author, Publisher, UsedBy
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db.models import Avg
from datetime import datetime, timedelta
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

import isbnlib
import barcode
from StringIO import StringIO

from polybookexchange.utils import sciper2mail, send_templated_mail


@login_required
def home(request):

    last_exemplar = Exemplar.objects.filter(buyer_id=None).order_by('-pk').first()
    random_exemplar = Exemplar.objects.filter(buyer_id=None).order_by('?').first()

    return render_to_response('polybookexchange/index.html', {'last_exemplar': last_exemplar, 'random_exemplar': random_exemplar}, context_instance=RequestContext(request))


@login_required
def book(request, isbn):

    book = get_object_or_404(Book, isbn=isbn)

    return render_to_response('polybookexchange/book.html', {'book': book}, context_instance=RequestContext(request))


@login_required
def howto(request):

    return render_to_response('polybookexchange/howto.html', {}, context_instance=RequestContext(request))


@login_required
def exemplar(request, id):

    exemplar = get_object_or_404(Exemplar, pk=id)

    return render_to_response('polybookexchange/exemplar.html', {'exemplar': exemplar}, context_instance=RequestContext(request))


@login_required
def exemplar_print(request, id):

    exemplar = get_object_or_404(Exemplar, pk=id)

    return render_to_response('polybookexchange/exemplar_print.html', {'exemplar': exemplar}, context_instance=RequestContext(request))


@login_required
def browse(request):

    sections = Section.objects.order_by('pk').all()
    semestres = Semester.objects.order_by('pk').all()

    try:
        section = Section.objects.get(pk=int(request.GET.get('sec', '-1')))
    except:
        section = None

    try:
        semestre = Semester.objects.get(pk=int(request.GET.get('sem', '-1')))
    except:
        semestre = None

    if request.GET.get('sec'):

        liste = Book.objects

        if section and not semestre:
            liste = liste.filter(usedby__section=section)

        if semestre and not section:
            liste = liste.filter(usedby__semester=semestre)

        if semestre and section:
            liste = liste.filter(usedby__section=section, usedby__semester=semestre)
        if not request.user.is_staff:
            liste = liste.filter(exemplar__buyer_id=None)

        liste = liste.order_by('pk').distinct().all()

        paginator = Paginator(liste, 10)

        # Make sure page request is an int. If not, deliver first page.
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1

        # If page request (9999) is out of range, deliver last page of results.
        try:
            liste = paginator.page(page)
        except (EmptyPage, InvalidPage):
            liste = paginator.page(paginator.num_pages)

    else:
        liste = None

    return render_to_response('polybookexchange/browse.html', {'sections': sections, 'semestres': semestres, 'section': section, 'semestre': semestre, 'liste': liste}, context_instance=RequestContext(request))


@login_required
def search(request):

    isbn = request.GET.get('isbn', '')
    author = request.GET.get('author', '')
    title = request.GET.get('title', '')

    try:
        section = Section.objects.get(pk=int(request.GET.get('sec', '-1')))
    except:
        section = None

    try:
        semestre = Semester.objects.get(pk=int(request.GET.get('sem', '-1')))
    except:
        semestre = None

    liste = Book.objects

    if isbn:
        liste = liste.filter(isbn__icontains=isbn)

    if section and not semestre:
        liste = liste.filter(usedby__section=section)

    if semestre and not section:
        liste = liste.filter(usedby__semester=semestre)

    if semestre and section:
        liste = liste.filter(usedby__section=section, usedby__semester=semestre)

    if author:
        liste = liste.filter(author__name__icontains=author)

    if title:
        liste = liste.filter(title__icontains=title)

    if not request.user.is_staff:
        liste = liste.filter(exemplar__buyer_id=None)

    liste = liste.order_by('pk').distinct().all()

    paginator = Paginator(liste, 10)

    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # If page request (9999) is out of range, deliver last page of results.
    try:
        liste = paginator.page(page)
    except (EmptyPage, InvalidPage):
        liste = paginator.page(paginator.num_pages)

    sections = Section.objects.order_by('pk').all()
    semestres = Semester.objects.order_by('pk').all()

    return render_to_response('polybookexchange/search.html', {'liste': liste, 'isbn': isbn, 'title': title, 'author': author, 'section': section, 'semestre': semestre, 'sections': sections, 'semestres': semestres}, context_instance=RequestContext(request))


@login_required
def purchases(request):

    liste = Exemplar.objects.filter(buyer_id=request.user.get_sciper()).order_by('sold_date').all()

    return render_to_response('polybookexchange/purchases.html', {'liste': liste}, context_instance=RequestContext(request))


@login_required
def sales(request):

    liste = Exemplar.objects.filter(seller_id=request.user.get_sciper()).order_by('posted_date').all()

    return render_to_response('polybookexchange/sales.html', {'liste': liste}, context_instance=RequestContext(request))


@login_required
def change_price(request, id):

    exemplar = get_object_or_404(Exemplar, pk=id, seller_id=request.user.get_sciper(), buyer_id=None)
    status = ""

    if request.method == 'POST':

        try:
            price = int(request.POST.get('price'))
        except:
            price = 0

        if price <= 0:
            status = "err"
        else:
            status = "ok"
            exemplar.price = price
            exemplar.save()
            exemplar.book.avg_price = Exemplar.objects.filter(book=exemplar.book).aggregate(Avg('price'))['price__avg']
            exemplar.book.save()

            send_templated_mail(_('Bookexchange: Change of price'), settings.POLYBOOKEXCHANGE_EMAIL_FROM, [settings.POLYBOOKEXCHANGE_EMAIL_MANAGERS], 'price_change', {'exemplar': exemplar})

    return render_to_response('polybookexchange/change_price.html', {'exemplar': exemplar, 'status': status}, context_instance=RequestContext(request))


@login_required
def proposed(request):

    proposals = Candidate.objects.filter(sciper=request.user.get_sciper()).order_by('pk').all()

    return render_to_response('polybookexchange/proposed.html', {'liste': proposals}, context_instance=RequestContext(request))


@login_required
def candidate_card(request, id):

    candidate = get_object_or_404(Candidate, pk=id, sciper=request.user.get_sciper())

    return render_to_response('polybookexchange/candidate_fiche.html', {'candidate': candidate}, context_instance=RequestContext(request))


@login_required
def check_isbn(request):

    isbn = request.GET.get('isbn', '')

    if not isbnlib.is_isbn13(isbn):
        return HttpResponse('<span class="text-warning"><i class="glyphicon glyphicon-warning-sign"></i> %s</span>' % (unicode(_('Not an ISBN')), ))

    data = isbnlib.meta(str(isbn))

    if not data or not data.get('Authors'):
        return HttpResponse('<span class="text-danger"><i class="glyphicon glyphicon-remove"></i> %s</span>' % (unicode(_('Cannot found this ISBN in online databases')), ))

    return HttpResponse('<span class="text-success"><i class="glyphicon glyphicon-ok"></i> %s</span>' % (unicode(_('Good ISBN !')), ))


@login_required
def propose(request):

    error = False

    sections = Section.objects.order_by('pk').all()
    semestres = Semester.objects.order_by('pk').all()

    isbn = ''
    annotated = False
    highlighted = ''
    state = ''
    comment = ''
    price = 0

    if request.method == 'POST':

        isbn = request.POST.get('isbn', '')
        if not isbnlib.is_isbn13(isbn):
            isbn = ''

        annotated = request.POST.get('annotated', '') == 'annotated'
        highlighted = request.POST.get('highlighted', '') == 'highlighted'
        state = request.POST.get('state', '')

        if state not in ['neuf', 'bon', 'acceptable', 'mauvais']:
            state = ''

        comment = request.POST.get('comment')
        try:
            price = int(request.POST.get('price'))
        except:
            price = 0

        if isbn == '' or state == '' or price <= 0 or request.POST.get('terms') != 'terms':
            error = True
        else:

            c = Candidate(isbn=isbn, sciper=request.user.get_sciper(), annotated=annotated, highlighted=highlighted, state=state, comments=comment, price=price)
            c.save()

            for sec in sections:
                for sem in semestres:
                    if request.POST.get('c_' + str(sec.pk) + '_' + str(sem.pk)):
                        CandidateUsage(candidate=c, section=sec, semester=sem).save()
            return render_to_response('polybookexchange/propose_ok.html', {'c': c}, context_instance=RequestContext(request))

    return render_to_response('polybookexchange/propose.html', {'error': error, 'sections': sections, 'semestres': semestres, 'isbn': isbn, 'annotated': annotated, 'highlighted': highlighted, 'price': price, 'comment': comment}, context_instance=RequestContext(request))


@login_required
@staff_member_required
def admin(request):

    return render_to_response('polybookexchange/admin.html', {}, context_instance=RequestContext(request))


@login_required
@staff_member_required
def remove_book(request):

    status = 'need_data'

    exemplar_id = request.GET.get('exemplar_id', request.POST.get('exemplar_id'))
    exemplar = None

    if exemplar_id:

        try:
            exemplar = Exemplar.objects.get(pk=exemplar_id, buyer_id=None)
        except:
            status = 'error'
            exemplar_id = ''

    if exemplar:

        status = 'ok'

        exemplar.buyer_id = exemplar.seller_id
        exemplar.sold_date = datetime.now()
        exemplar.save()

        exemplar.book.qty_in_stock -= 1
        exemplar.book.qty_sold += 1
        exemplar.book.save()

        send_templated_mail(_('AGEPoly\'s book exchange: Exemplar removed'), settings.POLYBOOKEXCHANGE_EMAIL_FROM, [sciper2mail(exemplar.seller_id)], 'book_removed', {'exemplar': exemplar})

    return render_to_response('polybookexchange/remove_book.html', {'exemplar_id': exemplar_id, 'status': status}, context_instance=RequestContext(request))


@login_required
@staff_member_required
def sell_book(request):

    status = 'need_data'

    exemplar_id = request.GET.get('exemplar_id', request.POST.get('exemplar_id'))
    exemplar = None

    if exemplar_id:

        try:
            exemplar = Exemplar.objects.get(pk=exemplar_id, buyer_id=None)
        except:
            status = 'error'
            exemplar_id = ''

    sciper = request.POST.get('sciper')

    if sciper and exemplar:

        status = 'ok'

        exemplar.buyer_id = sciper
        exemplar.sold_date = datetime.now()
        exemplar.save()

        exemplar.book.qty_in_stock -= 1
        exemplar.book.qty_sold += 1
        exemplar.book.save()

        send_templated_mail(_('AGEPoly\'s book exchange: Exemplar sold'), settings.POLYBOOKEXCHANGE_EMAIL_FROM, [sciper2mail(exemplar.seller_id)], 'book_sold', {'exemplar': exemplar})

    return render_to_response('polybookexchange/sell_book.html', {'exemplar_id': exemplar_id, 'status': status}, context_instance=RequestContext(request))


@login_required
@staff_member_required
def list_candidates(request):

    return render_to_response('polybookexchange/list_candidates.html', {'candidates': Candidate.objects.order_by('pk').all()}, context_instance=RequestContext(request))


@login_required
@staff_member_required
def transactions(request):

    liste = Exemplar.objects.order_by('-pk').all()

    paginator = Paginator(liste, 25)

    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # If page request (9999) is out of range, deliver last page of results.
    try:
        liste = paginator.page(page)
    except (EmptyPage, InvalidPage):
        liste = paginator.page(paginator.num_pages)

    return render_to_response('polybookexchange/transactions.html', {'liste': liste}, context_instance=RequestContext(request))


@login_required
@staff_member_required
def clean_candidates(request):

    if request.method == 'POST':

        for id in request.POST.getlist('to_delete[]'):
            get_object_or_404(Candidate, pk=id).delete()

        done = True

    else:
        done = False

    to_delete = Candidate.objects.filter(creation_date__lte=datetime.now() - timedelta(16)).all()

    return render_to_response('polybookexchange/clean_candidates.html', {'to_delete': to_delete, 'done': done}, context_instance=RequestContext(request))


@login_required
@staff_member_required
def add_book(request):

    candidate = None
    candidate_id = request.GET.get('candidate_id')

    if candidate_id:
        try:
            candidate = Candidate.objects.get(pk=request.GET.get('candidate_id'))
        except Candidate.DoesNotExist:
            pass

    isbn = request.GET.get('isbn')
    sciper = request.GET.get('sciper')

    if (isbn and isbnlib.is_isbn13(isbn) and sciper) or candidate:
        # Les paramètres de base on été envoyé (Candidat ou ISBN), on peut donc checker si le livre existe

        bonusC = '&candidate_id=%s' % (candidate.pk, ) if candidate else ''

        if candidate:
            isbn = candidate.isbn
            sciper = candidate.sciper
        else:
            sciper = int(sciper)

        if request.method == 'POST':
            # Le formulaire de création d'un livre à été envoyé

            book = get_object_or_404(Book, isbn=isbn)  # Has been created before
            book.title = request.POST.get('title')
            book.year = request.POST.get('year')
            book.edition = request.POST.get('edition')

            book.save()

            book.publisher, _ = Publisher.objects.get_or_create(name=request.POST.get('publisher', 'Unknow').strip())
            book.author.clear()

            for author in request.POST.get('authors', '').split(','):
                author = author.strip()

                if author:
                    author_object, _ = Author.objects.get_or_create(name=author)
                    book.author.add(author_object)

            book.update_cover()

        # On regarde ce qu'on est censé faire
        try:
            # If the book exist, let's add the exemplar
            book = Book.objects.get(isbn=isbn)
            return HttpResponseRedirect(reverse('polybookexchange.views.add_exemplar') + '?isbn=%s&sciper=%s%s' % (isbn, sciper, bonusC,))
        except Book.DoesNotExist:
            # Display the form
            book = Book(edition='1', isbn=isbn)
            book.update_metadata()

            return render_to_response('polybookexchange/add_book_new_book.html', {'book': book}, context_instance=RequestContext(request))

    else:
        # Aucun paramètre passé. On demande l'isbn et le sciper
        return render_to_response('polybookexchange/add_book_request.html', {'warning_candidate': candidate_id and not candidate}, context_instance=RequestContext(request))


@login_required
@staff_member_required
def add_exemplar(request):

    candidate = None
    candidate_id = request.GET.get('candidate_id')

    if candidate_id:
        try:
            candidate = Candidate.objects.get(pk=request.GET.get('candidate_id'))
        except Candidate.DoesNotExist:
            pass

    isbn = request.GET.get('isbn')
    sciper = request.GET.get('sciper')

    sections = Section.objects.order_by('pk').all()
    semestres = Semester.objects.order_by('pk').all()

    if request.GET.get('candidate_id', '') != '':
        try:
            candidate = Candidate.objects.get(pk=request.GET.get('candidate_id'))
        except:
            pass

    if isbn and sciper and isbnlib.is_isbn13(isbn) or candidate:

        if candidate:
            isbn = candidate.isbn
            sciper = candidate.sciper
        else:
            sciper = int(request.GET.get('sciper'))

        book = Book.objects.get(isbn=isbn)

        if request.method == 'POST':
            annotated = request.POST.get('annotated') == 'annotated'
            highlighted = request.POST.get('highlighted') == 'highlighted'
            state = request.POST.get('state')
            comment = request.POST.get('comment')
            price = request.POST.get('price')

            e = Exemplar(book=book, price=price, seller_id=sciper, annotated=annotated, highlighted=highlighted, state=state, comments=comment)
            e.save()

            book.qty_in_stock += 1
            book.avg_price = Exemplar.objects.filter(book=book).aggregate(Avg('price'))['price__avg']
            book.save()

            for sec in sections:
                for sem in semestres:
                    if request.POST.get('c_' + str(sec.pk) + '_' + str(sem.pk)):
                        UsedBy.objects.get_or_create(book=book, section=sec, semester=sem)

            send_templated_mail(_('AGEPoly\'s book exchange: Exemplar in sale'), settings.POLYBOOKEXCHANGE_EMAIL_FROM, [sciper2mail(e.seller_id)], 'book_insale', {'exemplar': e})

            if candidate:
                candidate.delete()

            return redirect('polybookexchange.views.exemplar', e.pk)

        else:
            return render_to_response('polybookexchange/add_exemplar.html', {'book': book, 'sciper': sciper, 'candidate': candidate, 'sections': sections, 'semestres': semestres}, context_instance=RequestContext(request))


@login_required
def gen_bar_code(request, code):
    """Generate a bar code"""

    fp = StringIO()

    wr = barcode.writer.ImageWriter()
    wr.format = 'JPEG'

    barcode.generate('isbn' if isbnlib.is_isbn13(code) else 'code39', str(code), writer=wr, output=fp, writer_options={'write_text': False, 'module_width': 0.1, 'module_height': 2.0, 'quiet_zone': 0.0})

    return HttpResponse(fp.getvalue(), content_type="image/png")
