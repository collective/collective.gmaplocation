from collective.gmaplocation.utils import get_propsheet


def _wrap(name):
    """Return getter and setter function for property sheet property.
    """
    def _get(self):
        return self._get(name)
    def _set(self, val):
        self._set(name, val)
    return _get, _set


class propsheet_attributes(object):
    """Decorator to set property sheet rw properties on class.
    """
    def __init__(self, *args):
        self.args = args
    
    def __call__(self, ob):
        for arg in self.args:
            setattr(ob, arg, property(*_wrap(arg)))
        return ob


@propsheet_attributes('default_width', 'default_width_unit', 'default_height', 
                      'default_height_unit', 'default_lat', 'default_lon', 
                      'default_zoom', 'default_language', 'default_region', 
                      'default_map_type')
class GMapProps(object):
    """Wrapper object for gmap_location_properties property sheet.
    """
    def __init__(self, context):
        self.context = context

    @property
    def propsheet(self):
        return get_propsheet()

    def _set(self, name, val):
        sheet = self.propsheet
        if sheet.hasProperty(name):
            sheet._updateProperty(name, val)
        else:
            sheet._setProperty(name, val)

    def _get(self, name):
        return self.propsheet.getProperty(name)