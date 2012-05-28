## Script (Python) "bSource"
##title=Get source info for metadata in catalog
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
    ret = view.getSource()
except Exception, e:
    if debug:
        context.plone_log('bSource %s' % e)
return ret
