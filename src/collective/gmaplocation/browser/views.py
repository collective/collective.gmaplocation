import json
from zope.i18nmessageid import MessageFactory
from Products.Five import BrowserView
from collective.gmaplocation.interfaces import IGMapLocationData

_ = MessageFactory('gmaplocation')


class GMapLocationView(BrowserView):
    """View providing ajax actions for location and zoom level manipulation.
    """
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.data = IGMapLocationData(context)
    
    def set_location(self):
        try:
            lat = float(self.request.get('lat'))
            lon = float(self.request.get('lon'))
        except ValueError:
            msg = _(u'Cannot parse lat/lng. Float conversion failed')
            return json.dumps({
                'status': 'ERROR',
                'message': self.context.translate(msg),
            })
        self.data.lat = lat
        self.data.lon = lon
        msg = _(u'Location Coordinates set: ${lat}, ${lon}',
                mapping={
                    'lat': str(lat),
                    'lon': str(lon)
                })
        return json.dumps({
            'status': 'SUCCESS',
            'message': self.context.translate(msg),
        })
    
    def set_zoom(self):
        try:
            zoom = int(self.request.get('zoom'))
        except ValueError:
            msg = _(u'Cannot parse zoom. Int conversion failed')
            return json.dumps({
                'status': 'ERROR',
                'message': self.context.translate(msg),
            })
        if zoom < 0 or zoom > 21:
            msg = _(u'Zoom out of range')
            return json.dumps({
                'status': 'ERROR',
                'message': self.context.translate(msg),
            })
        self.data.zoom = str(zoom)
        msg = _(u'Zoom level set to: ${zoom}',
                mapping={
                    'zoom': str(zoom),
                })
        return json.dumps({
            'status': 'SUCCESS',
            'message': self.context.translate(msg),
        })