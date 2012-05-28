from plone.indexer import indexer
from Products.CMFBibliographyAT.interface import IBibliographicItem 

@indexer(IBibliographicItem)
def BiblioSource(obj):
    return obj.Source()


@indexer(IBibliographicItem)
def AuthorsList(obj):
    return  [a.__dict__ for a in 
             [o for o in obj.getAuthors()]]

 
