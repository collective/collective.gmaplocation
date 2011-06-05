from zope.interface import (
    Interface,
    Attribute,
)


class IGMapLocationExtensionLayer(Interface):
    """Browser layer for collective.gmaplocation
    """


class IGMapLocation(Interface):
    """Marker interface for google map location.
    """


class IGMapLocationData(Interface):
    """Interface for google maps location data.
    """
    width = Attribute(u"Map width as r/w property")
    
    height = Attribute(u"Map height as r/w property")
    
    lat = Attribute(u"Latitude of location as r/w property")
    
    lon = Attribute(u"Longitude of location as r/w property")
    
    zoom = Attribute(u"Map Zoom Level as r/w property")
    
    map_type = Attribute(u"Map type as r/w property")
    
    map_language = Attribute(u"Map language as r/w property")
    
    map_region = Attribute(u"Map search region as r/w property")
    
    info_title = Attribute(u"Info window title as r/w property")
    
    info_description = Attribute(u"Info window description as r/w property")
    
    info_image = Attribute(u"Image to be displayed in info window as r/w "
                           u"property")
    
    info_target_link = Attribute(u"Hyperlink to be displayed in info "
                                 u"window as r/w property")