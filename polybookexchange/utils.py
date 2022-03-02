import ldap
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.utils.translation import ugettext as _


def search_attr_in_ldap(sciper, attr):

    con = ldap.initialize('ldap://ldap.epfl.ch:389')
    con.simple_bind()

    base_dn = 'c=ch'
    filter = '(uniqueIdentifier=%s)' % (str(sciper), )
    attrs = [attr]

    val = ''

    try:
        for someone in con.search_s(base_dn, ldap.SCOPE_SUBTREE, filter, attrs):
            val = someone[1][attr][0]
    except:
        pass

    return val


def sciper2mail(sciper):
    """Convert a sciper to an email, searching in EPFL's LDAP"""
    return search_attr_in_ldap(sciper, 'mail') or 'nobody@epfl.ch'


def sciper2name(sciper):
    """Convert a sciper to a name, using EPFL's LDAP"""
    return search_attr_in_ldap(sciper, 'cn') or _("Unknown name")


def send_templated_mail(subject, email_from, emails_to, template, context):
    """Send a email using an template (both in text and html format)"""

    plaintext = get_template('polybookexchange/emails/%s.txt' % (template, ))
    htmly = get_template('polybookexchange/emails/%s.html' % (template, ))

    d = Context(context)

    text_content = plaintext.render(d)
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(subject, text_content, email_from, emails_to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
