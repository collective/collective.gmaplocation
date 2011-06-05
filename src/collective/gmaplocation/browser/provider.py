from Acquisition import Explicit
from zope.interface import (
    Interface,
    implements,
)
from zope.security import checkPermission
from zope.component import (
    adapts,
    getMultiAdapter,
)
from zope.publisher.interfaces.browser import (
    IBrowserRequest,
    IBrowserView,
)
from zope.contentprovider.interfaces import IContentProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.gmaplocation.interfaces import (
    IGMapLocation,
    IGMapLocationData,
)
from collective.gmaplocation.properties import GMapProps
from collective.gmaplocation.utils import get_portal


class Base(Explicit):
    """Base object for google map related content providers.
    """
    implements(IContentProvider)
    adapts(IGMapLocation, IBrowserRequest, IBrowserView)
    template = None
    
    def __init__(self, context, request, view):
        self.__parent__ = view
        self.context = context
        self.request = request
        self.data = IGMapLocationData(context)
    
    def update(self):
        pass
    
    def render(self):
        return self.template(self)


class ScriptResources(Base):
    """Provides JavaScript resource links related to google maps language
    settings.
    """
    template = ViewPageTemplateFile(u'templates/resources.pt')
    
    @property
    def gmap_script_source(self):
        return 'http://maps.google.com/maps/api/js?sensor=false&language=%s' \
            % self.data.map_language
    
    @property
    def gmap_script_lang(self):
        return '/++resource++collective.gmaplocation.scripts/%s.js' \
            % self.data.map_language


class Authoring(Base):
    """Provides authoring related elements.
    """
    template = ViewPageTemplateFile(u'templates/authoring.pt')
    
    @property
    def display_authoring(self):
        return checkPermission('cmf.ModifyPortalContent', self.context)
    
    @property
    def context_url(self):
        return self.context.absolute_url()


class Map(Base):
    """Provides the map element.
    """
    template = ViewPageTemplateFile(u'templates/map.pt')
    
    @property
    def dimensions(self):
        return 'width:%ipx;height:%ipx' % (self.data.width, self.data.height)


class Invocation(Base):
    """Provides map invocation code.
    """
    template = ViewPageTemplateFile(u'templates/invocation.pt')
    
    @property
    def script(self):
        lat = self.data.lat
        lon = self.data.lon
        props = GMapProps(get_portal())
        if not lat:
            lat = props.default_lat
        if not lon:
            lon = props.default_lon
        return """\
            var map_type = google.maps.MapTypeId.%(type)s;
            gmaplocation.set_defaults({
                lat: %(lat)s,
                lon: %(lon)s,
                zoom: %(zoom)s,
                type: map_type,
                info: '%(info)s',
                title: '%(title)s',
                region: '%(region)s',
                language: '%(language)s'
            });
            gmaplocation.show_location();
        """ % {
            'lat': str(lat),
            'lon': str(lon),
            'zoom': self.data.zoom,
            'type': self.data.map_type,
            'info': self.rendered_info,
            'title': self.context.Title(),
            'region': self.data.map_region,
            'language': self.data.map_language,
        }
    
    @property
    def rendered_info(self):
        toadapt = (self.context, self.request, self.__parent__)
        renderer = getMultiAdapter(toadapt,
                                   IContentProvider,
                                   name='collective.gmaplocation.info')
        renderer.update()
        return renderer.render().replace('\n', ' ')


class Route(Base):
    """Provides route planner.
    """
    template = ViewPageTemplateFile(u'templates/route.pt')


class Info(Base):
    """Provides info window markup.
    """
    template = ViewPageTemplateFile(u'templates/info.pt')
    
    @property
    def info_description(self):
        desc = self.context.getField('info_description').get(self.context)
        return desc.replace('\r\n', ' ')