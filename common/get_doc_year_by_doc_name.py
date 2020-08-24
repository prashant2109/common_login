#!/usr/bin/python
# -*- coding:utf-8 -*-
import os, sys, re

def get_doc_year_by_doc_name(doc_name):
    try:
        if 'PR' in doc_name:
            doc_year = get_doc_name_with_re(doc_name)
        else:
            regex = re.search('([A-Z]{1,2}\d?_?\d{4}|\d{4}\d?_?[A-Z]{1,2})', doc_name)
            #regex = re.search('([A-Z]{1,2}\d?_?\d{4})', doc_name)
            doc_year = regex.group()
    except:
        doc_year = ''
    if ((len(doc_year.split('_')) == 2) and (doc_year.split('_')[1] in ['Q1', 'Q2', 'Q3','Q4', 'AR', 'FY', 'H1', 'H2'])):
        doc_year = doc_year.split('_')[1] + '_' + doc_year.split('_')[0]
    doc_year_info = ''.join([x for x in doc_year.split('_')])
    if 'AR' in doc_year_info:
        doc_year_info = doc_year_info.replace('AR', 'FY')
    return doc_year_info

def get_doc_name_with_re(doc_name):
    regex = re.search('(\d{4}\w*PR$)', doc_name)
    doc_year = regex.group()
    new_doc_name = ''
    if len(doc_year.split('_')) == 3:
        if doc_year.split('_')[2] == 'PR':
            changed_name = 'AR'
        new_doc_name = changed_name + '_' + doc_year.split('_')[0]
    return new_doc_name


