# -*- coding: utf-8 -*-
import os
import transaction
import yafowil.loader
from yafowil.yaml import parse_from_YAML
from zope.i18nmessageid import MessageFactory
from Products.Five import BrowserView
from yafowil.controller import Controller
from zExceptions import Redirect
from collective.gmaplocation.properties import GMapProps
from collective.gmaplocation.utils import get_portal

_ = MessageFactory('gmaplocation')


class GMapControlPanel(BrowserView):
    """Google maps default settings control panel form.
    """

    @property
    def action_resource(self):
        return '%s/%s' % (self.context.absolute_url(), '@@gmap-controlpanel')
    
    @property
    def props(self):
        return GMapProps(get_portal())
    
    @property
    def form(self):
        path = os.path.join(os.path.dirname(__file__), 'controlpanel.yaml')
        form = parse_from_YAML(path, self, _)
        controller = Controller(form, self.request)
        if not controller.next:
            return controller.rendered
        raise Redirect(controller.next)
    
    def form_action(self, widget, data):
        return self.action_resource

    def save(self, widget, data):
        props = self.props
        def at(name):
            return '%s.%s' % (widget.name, name)
        for name in widget:
            if name == 'save':
                continue
            setattr(props, name, data.fetch(at(name)).extracted)
        transaction.commit()

    def next(self, request):
        return self.action_resource