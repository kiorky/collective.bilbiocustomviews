#!/usr/bin/env python
# -*- coding: utf-8 -*-
__docformat__ = 'restructuredtext en'


from zope import component, interface
from zope.component import getAdapter, getMultiAdapter, queryMultiAdapter, getUtility
from Products.CMFPlone.PloneBatch import Batch
from Products.ATContentTypes.interface import IATTopic

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
    def getFolderContents(contentFilter=None, batch=False,b_size=100,full_objects=False):
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

    def author_repeat_sep(self, repeat, key):
        sep = ''
        if self.inmiddle(repeat, 'i'):
            sep = ',&nbsp;'
        if not self.first(repeat, 'i') and self.last(repeat, 'i'):
            sep = '&amp;&nbsp;'
        return sep

    def getFolderContents(self, contentFilter=None, batch=False,b_size=100,full_objects=False):
        import pdb;pdb.set_trace()  ## Breakpoint ##
        context = self.context
        mtool = context.portal_membership
        cur_path = '/'.join(context.getPhysicalPath())
        path = {}
        if not contentFilter:
            contentFilter = {}
        else:
            contentFilter = dict(contentFilter)
        if not contentFilter.get('sort_on', None):
            contentFilter['sort_on'] = 'getObjPositionInParent'
        if contentFilter.get('path', None) is None:
            path['query'] = cur_path
            path['depth'] = 1
            contentFilter['path'] = path
        show_inactive = mtool.checkPermission('Access inactive portal content', context)
        # Provide batching hints to the catalog
        b_start = int(context.REQUEST.get('b_start', 0))
        # Evaluate in catalog context because
        # some containers override queryCatalog
        # with their own unrelated method (Topics)
        method = context.portal_catalog.queryCatalog
        if IATTopic.providedBy(self.context):
            method = self.context.queryCatalog
        contents = list(method(
            contentFilter,
            show_all=1,
            show_inactive=show_inactive,))
        if full_objects:
            contents = [b.getObject() for b in contents]
        # sort by author and year
        def comparecustom(a):
            return '%s___%s' % (a.Authors, a.Title)
        contents.sort(key=comparecustom)
        if batch:
            batch = Batch(contents, b_size, b_start, orphan=0)
            return batch
        return contents

    def getContentFilter(self, contentFilter):
        sort_on = self.request.get('sort_on', contentFilter.get('sort_on', 'Authors'))
        contentFilter['sort_on'] = sort_on
        return contentFilter

    def inmiddle(self, repeat, key):
        """"""
        return (not repeat[key].start and
            not repeat[key].end)

    def last(self, repeat, key):
        """"""
        return repeat[key].end

    def first(self, repeat, key):
        """"""
        return repeat[key].start

    def instrictmiddle(self, repeat, key):
        """"""
        return (self.inmiddle(repeat, key) and
                not self.beforelast(repeat, key))

    def beforelast(self, repeat, key):
        """"""
        ret = False
        rp = repeat[key]
        if self.inmiddle(repeat, key):
            if rp.number() == rp.length()-1:
                ret = True
        return ret

    def infosFor(self, it):
        item = it
        authors_links = []
        if 'brain' in it.__class__.__name__:
            item = it.getObject()
        authors = [dict(e) for e in item.getAuthors()]
        for e in authors:
            for k in ['firstname', 
                      'lastname', 
                      'middlename', 
                      'homepage']:
                if not k in e:
                    e[k] = ''
        for e in authors:
            author = ('%(lastname)s '
                      '%(firstname)s '
                      '%(middlename)s' % e).strip()
            if e['homepage']:
                author = '<a href="%s">%s</a>' % (
                    e['homepage'],
                    author,
                )
            authors_links.append(author)
        title = item.title_or_id()
        data = {
            'authors': authors,
            'authors_links': authors_links,
            'title': title.strip(),
            'publication_year': item.getPublication_year(),
            'source': item.Source(),
            'url': item.absolute_url(),
        }
        return  data


class IBibliocvMacros(ISummaryView):
    """."""

class BibliocvMacros(SummaryView):
    """.""" 

class IDatatable(ISummaryView):
    """."""

class Datatable(SummaryView):
    """."""

class ISearch(ISummaryView):
    """."""

class Search(SummaryView):
    """.""" 
# vim:set et sts=4 ts=4 tw=80:

