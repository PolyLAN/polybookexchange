PolyBookExchange
================

PolyBookExchange is a small django application used for book exchange at AGEPoly, the student association of EPFL.

## License

PolyBookExchange is distributed with the [BSD](http://opensource.org/licenses/BSD-2-Clause) license.

## Authors

PolyBookExchange has been developped by [Maximilien Cuony](https://github.com/the-glu) .

This version is adapted from a previous django version made in 2010, who was made from the original version, developped in Java (in 2007?), by Loïc Etienne et Aristidis Papaioannou.

## Assumptions

The module can be used in any django 1.7 project, but some additionnal work may be needed:

* The system assume all users have a `get_sciper()` method, returing an unique ID for the current user. The system will use the EPFL's LDAP and the sciper to make queries for user's details.

## Setup

### Install the package

`pip install https://github.com/PolyLAN/polybookexchange.git`

### Update your setttings

You need to activate this app, and _django.contrib.humanize_.

Add to your INSTALLED_APPS:

```
    'polybookexchange',
    'django.contrib.humanize',
```

(Of course, you don't need to add a line twice if one app is already installed !)


### Set parameters

Add to your settings.py

```
POLYBOOKEXCHANGE_EMAIL_FROM = ''
POLYBOOKEXCHANGE_EMAIL_MANAGERS = ''
```

and update values as you need. The first one is the sender for all email send by the book exchange and the second one is the email of someone who should be alerted e.g. when the price of a book change.

### Update your urls.py

Add something like this:

`url(r'^books/', include('polybookexchange.urls')),`

### Do the migrations

`python manage.py migrate`

### Install initial data

`python manage.py loaddata polybookexchange_epfl.yaml`
