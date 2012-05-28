## Script (Python) "bAuthorsList"
##title=Get authors info for metadata in catalog
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=

ret = None
debug=False
try:
    view = context.restrictedTraverse('@@bibliocv_utils')
    ret = view.getAuthorsList()
except Exception, e:
    if debug:
        context.plone_log('bAuthorsList %s' % e)
return ret
