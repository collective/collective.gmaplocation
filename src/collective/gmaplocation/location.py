from zope.interface import (
    implements,
    implementer,
)
from zope.component import (
    adapter,
    getAdapter,
)
from Products.Archetypes.interfaces import IBaseObject
from collective.gmaplocation.interfaces import IGMapLocationData


@implementer(IGMapLocationData)
@adapter(IBaseObject)
def at_gmap_location_data(context):
    """Factory for archetypes schema extender based location data.
    
    Looks up IGMapLocationData for context by portal type name. This is needed
    if multiple FTI's with same type implementations are used, but you only
    want to enable some of those as location data.
    """
    return getAdapter(context, IGMapLocationData, name=context.portal_type)


def _at_extender_wrap(name):
    """Return getter and setter function for schema extender attribute.
    """
    def _get(self):
        return self.context.getField(name).get(self.context)
    def _set(self, val):
        self.context.getField(name).set(self.context, val)
    return _get, _set


class at_extender_attributes(object):
    """Decorator to set schema extender rw properties on class.
    """
    def __init__(self, *args):
        self.args = args
    
    def __call__(self, ob):
        for arg in self.args:
            setattr(ob, arg, property(*_at_extender_wrap(arg)))
        return ob


@at_extender_attributes('width', 'height', 'lat', 'lon', 'zoom', 'map_type',
                        'map_language', 'map_region', 'info_title',
                        'info_description', 'info_image', 'info_target_link')
class ATGMapLocationData(object):
    """IGMapLocationData implementation for schema extender location data.
    """
    implements(IGMapLocationData)
    
    def __init__(self, context):
        self.context = context