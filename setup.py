#!/usr/bin/env python

from distutils.core import setup, Extension

setup(
    name='paystubs',
    version='1.0',
    description='Personal Accounting CLI',
    author='Ryan M',
    author_email='gn341ram@gmail.com',
    packages=['paystubs', 'paystubs/modules', 'paystubs/formatting', 'paystubs/financial_stmts', 'paystubs/data'],
    url='',
    ext_modules=[Extension('default_coa', ['default_coa.csv'])],
    depends=['matplotlib'],

)
