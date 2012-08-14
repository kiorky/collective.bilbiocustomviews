#!/usr/bin/env python
# -*- coding: utf-8 -*-
__docformat__ = 'restructuredtext en'

import logging

from zope import component, interface
from zope.component import getAdapter, getMultiAdapter, queryMultiAdapter, getUtility
from Products.ATContentTypes.interface import IATTopic

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from plone.registry.interfaces import IRegistry
from Products.ATContentTypes.interfaces.interfaces import IATContentType
from Acquisition import aq_parent
from Acquisition import aq_parent
from Products.CMFPlone.PloneBatch import Batch
from Products.CMFBibliographyAT.browser.export import BibliographyExportView
from Products.CMFBibliographyAT.interface import IBibliographicItem 

from plone.memoize import ram
from time import time

def five_minutes():
    return time() // (5 * 60)

def fifteen_minutes():
    return time() // (15 * 60) 

def _render_details_cachekey(method, self, brain):
    return (brain.getPath(), fifteen_minutes())

def _render_contents(method, self, *args, **kwargs):
    hs = fifteen_minutes()
    ids = [a for a in self.context.objectIds()]
    ids.sort()
    return (self.context.getPhysicalPath(), ids, hs)
def comparecustom(a):
    """
    sort by author and year."""
    return '%s___%s' % (a.Authors, a.Title) 

class IBibliocvUtils(interface.Interface):
    """Marker interface"""
    def getSource(self):
        """."""

    def getAuthorsList(self):
        """."""

def format_firstname(text):
    parts = []
    for part in text.split():
        if part:
            parts.append("%s." % part[0].upper())
    return '-'.join(parts)

class BibliocvUtils(BrowserView):
    interface.implements(IBibliocvUtils)
    ifs = ('lastname', 'firstname', 'middlename', 'homepage')

    def getSource(self):
        if IBibliographicItem.providedBy(self.context):
            return self.context.Source()
 
    def getAuthorsList(self):
        if IBibliographicItem.providedBy(self.context):
            authors = [dict(e) for e in self.context.getAuthors()]  
            results = []
            for e in authors:
                result = []
                for k in self.ifs:
                    if not k in e:
                        e[k] = ''
                    result.append(e[k])
                results.append(tuple(result))
            if results:
                return results

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
            sep = ', '
        if not self.first(repeat, 'i') and self.last(repeat, 'i'):
            sep = ' &amp; '
        return sep

    @ram.cache(_render_contents)
    def getFolderContents(self, contentFilter=None, batch=False,b_size=100,full_objects=False):
        #logging.getLogger('foo').error('cont hitted')
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
        contents.sort(key=comparecustom)
        if not b_size:
            b_size = len(contents)
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

    @ram.cache(_render_details_cachekey)
    def infosFor(self, it):
        #logging.getLogger('foo').error('info hitted')
        authors_links = []
        #if 'brain' in it.__class__.__name__:
        #    item = it.getObject()
        if it.bAuthorsList:
            for ue in it.bAuthorsList:
                e = {
                    'lastname':   ue[0],
                    'firstname':  ue[1],
                    'middlename': ue[2],
                    'formatedfname': format_firstname(
                        (ue[1] + " " + ue[2]).strip()
                    ),
                    'homepage':   ue[3],
                }
                author = ('%(lastname)s '
                          '%(formatedfname)s' % e).strip()
                if e['homepage']:
                    author = '<a href="%s">%s</a>' % (
                        e['homepage'],
                        author,
                    )
                authors_links.append(author)
        title = it.Title
        data = {
            'authors_links': authors_links,
            'title': title.strip(),
            'publication_year': it.publication_year,
            'source': it.bSource,
            'url': it.getURL(),
        }
        return  data

class IBibliocvMacros(ISummaryView):
    """."""

class BibliocvMacros(SummaryView):
    """.""" 
    def __init__(self, *args, **kwargs):
        SummaryView.__init__(self, *args, **kwargs)

class IDatatable(ISummaryView):
    """."""

class Datatable(SummaryView):
    """."""

class ISearch(ISummaryView):
    """."""

class Search(SummaryView):
    """.""" 
    def arrange(self, folderContents):
        """ Search using given criteria
        """
        ret = []
        if isinstance(folderContents, Batch):
            # make a list of all batch content
            ret = list(folderContents._sequence)
            ret.sort(key=comparecustom)
        elif folderContents:
            raise Exception(
                'Unexpected folderContents: %s' % type(
                    folderContents))
        return ret

    def export(self, *args, **kwargs):
        uids = self.request.form.get(
            'item', {}).get('selected', [])
        c = getToolByName(self.context, 'portal_catalog')
        brains =  c.searchResults(UID=uids)
        hv = BibliographyExportView(self.context, self.request)
 
        output_encoding = self.request.get('output_encoding', 'utf-8')
        eol_style = self.request.get('eol_style', 0)
        format = self.request.get('format', 'bibtex')
        response = self.request.response
        renderer = hv._getRenderer(format)
        # Hotfix: suffix for Endnote must be  '.enw', not '.end'
        suffix = renderer.target_format == 'end' and 'enw' or renderer.target_format
        response.setHeader('Content-Type', 'application/octet-stream')
        response.setHeader('Content-Disposition',
                           'attachment; filename=%s.%s' % ('(export', suffix)) 

        export = renderer.render(
            [a.getObject() for a in brains], 
            output_encoding=output_encoding,
            msdos_eol_style=eol_style)
        return export


# vim:set et sts=4 ts=4 tw=80:
