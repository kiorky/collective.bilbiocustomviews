import logging
from zope.i18nmessageid import MessageFactory
MessageFactory = collectivebibliocustomviewsMessageFactory = MessageFactory('collective.bibliocustomviews') 
logger = logging.getLogger('collective.bibliocustomviews')
def initialize(context):
    """Initializer called when used as a Zope 2 product.""" 
