# -*- coding: utf-8 -*-
from zope.interface import implements
from zope.component import adapts
from zope.i18nmessageid import MessageFactory
from archetypes.schemaextender.interfaces import (
    IOrderableSchemaExtender,
    IBrowserLayerAwareExtender,
)
from archetypes.schemaextender.field import ExtensionField
from Products.Archetypes.utils import OrderedDict
from Products.Archetypes.public import (
    FloatField,
    ImageField,
    StringField,
    TextField,
    StringWidget,
    IntegerWidget,
    DecimalWidget,
    ImageWidget,
    SelectionWidget,
    RichWidget,
)
from collective.gmaplocation.interfaces import (
    IGMapLocationExtensionLayer,
    IGMapLocation,
    IGMapLocationData,
)
from collective.gmaplocation.properties import GMapProps
from collective.gmaplocation.utils import (
    zoom_vocab,
    language_vocab,
    region_vocab,
    map_type_vocab,
    get_portal,
)

_ = MessageFactory('gmaplocation')


class XFloatField(ExtensionField, FloatField):
    """FloatField for use within schema extender.
    """


class XStringField(ExtensionField, StringField):
    """StringField for use within schema extender.
    """


class XTextField(ExtensionField, TextField):
    """TextField for use within schema extender.
    """


class XImageField(ExtensionField, ImageField):
    """ImageField for use within schema extender.
    """


def get_props():
    """Return global google maps properties.
    """
    return GMapProps(get_portal())


class GMapLocationExtender(object):
    """Schema extender for google maps location data.
    """
    
    implements(IOrderableSchemaExtender, IBrowserLayerAwareExtender)
    adapts(IGMapLocation)
    
    layer = IGMapLocationExtensionLayer

    fields = [
        XFloatField(
            name='lat',
            schemata='Location',
            default_method=lambda: get_props().default_lat,
            widget=DecimalWidget(
                label=_(u'label_latitude', u'Latitude'),
            )
        ),
        XFloatField(
            name='lon',
            schemata='Location',
            default_method=lambda: get_props().default_lon,
            widget=DecimalWidget(
                label=_(u'label_longitude', u'Longitude'),
            )
        ),
        XFloatField(
            name='width',
            schemata='Location',
            required=1,
            default_method=lambda: get_props().default_width,
            widget=IntegerWidget(
                size=3,
                label=_(u'label_width', u'Map width'),
            )
        ),
        XFloatField(
            name='height',
            schemata='Location',
            required=1,
            default_method=lambda: get_props().default_height,
            widget=IntegerWidget(
                size=3,
                label=_(u'label_height', u'Map height'),
            )
        ),
        XStringField(
            name='zoom',
            schemata='Location',
            vocabulary=zoom_vocab(),
            default_method=lambda: get_props().default_zoom,
            widget=SelectionWidget(
                label=_(u'label_zoom', u'Map zoom level'),
            )
        ),
        XStringField(
            name='map_language',
            schemata='Location',
            vocabulary=language_vocab(),
            default_method=lambda: get_props().default_language,
            widget=SelectionWidget(
                label=_(u'label_language', u'Map language'),
            )
        ),
        XStringField(
            name='map_region',
            schemata='Location',
            vocabulary=region_vocab(),
            default_method=lambda: get_props().default_region,
            widget=SelectionWidget(
                label=_(u'label_region', u'Map region'),
            )
        ),
        XStringField(
            name='map_type',
            schemata='Location',
            vocabulary=map_type_vocab(),
            default_method=lambda: get_props().default_map_type,
            widget=SelectionWidget(
                label=_(u'label_map_type', u'Map display type'),
            )
        ),
        XStringField(
            name='info_title',
            schemata='Location',
            widget=StringWidget(
                label=_(u'label_info_title', u'Info window title'),
            )
        ),
        XTextField(
            name='info_description',
            schemata='Location',
            widget=RichWidget(
                cols=10,
                label=_(u'label_info_description', u'Info window description'),
            )
        ),
        XImageField(
            name='info_image',
            schemata='Location',
            widget=ImageWidget(
                label=_(u'label_info_image', u'Info window image'),
            )
        ),
        XStringField(
            name='info_target_link',
            schemata='Location',
            widget=StringWidget(
                label=_(u'label_info_target_link', u'Info window target link'),
            )
        ),
    ]
    
    def __init__(self, context):
        self.context = context

    def getFields(self):
        try:
            IGMapLocationData(self.context)
            return self.fields
        except TypeError: # Why type error?
            return []
    
    def getOrder(self, original):
        neworder = OrderedDict()
        keys = original.keys()
        last = keys.pop()
        keys.insert(1, last)
        for schemata in keys:
            neworder[schemata] = original[schemata]
        return neworder