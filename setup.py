#!/usr/bin/python

from distutils.core import setup

setup(
    name='PolyBookExchange',
    version='0.1.9',
    description='A small django application for book exchange at AGEPoly.',
    long_description='PolyBookExchange is a small django application used for book exchange at AGEPoly, the student association of EPFL.',
    author='Maximilien Cuony',
    author_email='theglu@theglu.org',
    url='https://github.com/PolyLAN/polybookexchange',
    download_url='https://github.com/PolyLAN/polybookexchange',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    packages=[
        'polybookexchange',
    ],
    include_package_data=True,
    install_requires=[
        'south',
        'django',
        'isbnlib',
        'requests',
        'pyBarcode',
    ]
)
