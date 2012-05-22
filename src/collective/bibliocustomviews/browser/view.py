#!/usr/bin/env python
# -*- coding: utf-8 -*-
__docformat__ = 'restructuredtext en'


from zope import component, interface
from zope.component import getAdapter, getMultiAdapter, queryMultiAdapter, getUtility

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from plone.registry.interfaces import IRegistry
from Products.ATContentTypes.interfaces.interfaces import IATContentType
from Acquisition import aq_parent
from Acquisition import aq_parent


class ISummaryView(interface.Interface):
    """Marker interface"""
    def test(a, b, c):
        """."""
    def getContentFilter(contentFilter):
        """."""
    def infosFor(it):
        """."""

class SummaryView(BrowserView):
    """MY view doc"""
    interface.implements(ISummaryView)
    #template = ViewPageTemplateFile('template.pt')
    #def __call__(self, **params):
    #    """."""
    #    params = {}
    #    return self.template(**params)

    def test(self, a, b, c):
        if bool(a):
            return b
        else:
            return c

    def getContentFilter(self, contentFilter):
        sort_on = self.request.get('sort_on', contentFilter.get('sort_on', 'Authors'))
        contentFilter['sort_on'] = sort_on
        return contentFilter

    def infosFor(self, it):
        item = it
        if 'brain' in it.__class__.__name__:
            item = it.getObject()
        authors = [dict(e) for e in item.getAuthors()]
        for e in authors:
            for k in ['firstname', 'lastname', 'middlename', 'homepage']:
                if not k in e:
                    e[k] = ''
        authors_part = ['%(firstname)s %(middlename)s %(lastname)s' % e
                        for e in authors]
        authors_links = []
        for e in authors:
            author = '%(firstname)s %(middlename)s %(lastname)s' % e
            if e['homepage']:
                author = '<a href="%s">%s</a>' % (
                    e['homepage'],
                    author,
                )
            authors_links.append(author)
        title = item.title_or_id()
        data = {
            'authors': authors,
            'authors_part': authors,
            'authors_links': authors_links,
            'title': title,
            'publication_year': item.getPublication_year(),
        }
        return  data

# vim:set et sts=4 ts=4 tw=80:

