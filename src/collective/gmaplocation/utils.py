from zope.component import getUtility
from zope.i18nmessageid import MessageFactory
from Products.CMFCore.interfaces import ISiteRoot

_ = MessageFactory('gmaplocation')


def zoom_vocab():
    """List of available zoom levels as 2-tuples.
    """
    return [str(num) for num in range(21)]


def language_vocab():
    """List of available languages as 2-tuples.
    """
    return [
        ('de', _('German')),
        ('en', _('English')),
        ('en-AU', _('English (Australian)')),
        ('en-GB', _('English (Great Britain)')),
    ]


def region_vocab():
    """List of available regions as 2-tuples.
    """
    return [
        ('de', _('Germany')),
        ('eu', _('European Union')),
        ('su', _('Soviet Union')),
        ('uk', _('United Kingdom')),
        ('us', _('United States')), 
    ]


def map_type_vocab():
    """List of available map types as 2-tuples.
    """
    return [
        ('ROADMAP', _('Roadmap')),
        ('SATELLITE', _('Satellite')),
        ('HYBRID', _('Hybrid')),
        ('TERRAIN', _('Terrain')),
    ]


def get_portal():
    """Return portal object.
    """
    return getUtility(ISiteRoot)


def get_propsheet():
    """Return gmap_location_properties from portal properties
    """
    properties = get_portal().portal_properties
    return properties.restrictedTraverse('gmap_location_properties')


"""
Available Language codes:

ar    ARABIC
eu    BASQUE
bg    BULGARIAN
bn    BENGALI
ca    CATALAN
cs    CZECH
da    DANISH
de    GERMAN
el    GREEK
en    ENGLISH
en-AU    ENGLISH (AUSTRALIAN)
en-GB    ENGLISH (GREAT BRITAIN)
es    SPANISH
eu    BASQUE
fa    FARSI
fi    FINNISH
fil    FILIPINO
fr    FRENCH
gl    GALICIAN
gu    GUJARATI
hi    HINDI
hr    CROATIAN
hu    HUNGARIAN
id    INDONESIAN
it    ITALIAN
iw    HEBREW
ja    JAPANESE
kn    KANNADA
ko    KOREAN
lt    LITHUANIAN
lv    LATVIAN
ml    MALAYALAM
mr    MARATHI
nl    DUTCH
nn    NORWEGIAN NYNORSK
no    NORWEGIAN
pl    POLISH
pt    PORTUGUESE
pt-BR    PORTUGUESE (BRAZIL)
pt-PT    PORTUGUESE (PORTUGAL)
ro    ROMANIAN
ru    RUSSIAN
sk    SLOVAK
sl    SLOVENIAN
sr    SERBIAN
sv    SWEDISH
tl    TAGALOG
ta    TAMIL
te    TELUGU
th    THAI
tr    TURKISH
uk    UKRAINIAN
vi    VIETNAMESE
zh-CN    CHINESE (SIMPLIFIED)
zh-TW    CHINESE (TRADITIONAL)
"""