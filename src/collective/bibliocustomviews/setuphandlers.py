import logging
import transaction
from Products.CMFCore.utils import getToolByName

from collective.bibliocustomviews import app_config
from collective.bibliocustomviews.app_config import PRODUCT_DEPENDENCIES, EXTENSION_PROFILES

from Products.CMFBibliographyAT.interface import IBibliographicItem 

def setupVarious(context):
    """Miscellanous steps import handle.
    """
    l = logging.getLogger('collective.bibliocustomviews / setuphandler')
    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.
    if context.readDataFile('collective.bibliocustomviews_various.txt') is None:
        return

    portal = context.getSite()
    catalog = portal.portal_catalog
    #class extra:
    #    index_type="Okapi BM25 Rank"
    #    lexicon_id="plone_lexicon" 
    #for k, tp, extra in  [
    #    ('BiblioSource', 'ZCTextIndex', extra),
    #    ('AuthorsList',  'KeywordIndex', None),
    #]:
    #    if not k in catalog.Indexes:
    #        l.error('Creating %s in catalog' % k)
    #        catalog.addIndex(k, tp, extra)
    #        catalog.addColumn(k)
    #        catalog.reindexIndex(k, portal.REQUEST)
    columns =  catalog._catalog.schema
    reindex = True
    for k in ('bSource', 'bAuthorsList', ):
        if not k in columns:
            l.warn('Creating %s in catalog' % k)
            catalog.addColumn(k)
            reindex = True
    if reindex:
        l.warn('Reindexing')
        # reindex documents
        brains = catalog.searchResults(
            **{'object_provides':IBibliographicItem.__identifier__}
        )
        lb = len(brains)
        done = 0
        for i, b in enumerate(brains):
            cur = i * 100.0 / lb
            adone = int(cur) / 10 
            if done != adone:
                # print each 10%
                done = adone
                l.warn('Done %s/%s (%s%s)' %(i, lb, cur, '%'))
                transaction.commit()
            b.getObject().reindexObject()
    transaction.commit()

def setupQi(context):
    """Miscellanous steps import handle.
    """
    logger = logging.getLogger('collective.bibliocustomviews / setuphandler')

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile('collective.bibliocustomviews_qi.txt') is None:
        return

    portal = context.getSite() 
    portal_quickinstaller = getToolByName(portal, 'portal_quickinstaller')
    portal_setup = getToolByName(portal, 'portal_setup')
    logger = logging.getLogger('collective.bibliocustomviews.Install')

    for product in PRODUCT_DEPENDENCIES:
        logger.info('(RE)Installing %s.' % product)
        if not portal_quickinstaller.isProductInstalled(product):
            portal_quickinstaller.installProduct(product)
            transaction.savepoint()

