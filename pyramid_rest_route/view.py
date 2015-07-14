import logging

from pyramid.httpexceptions import HTTPNotImplemented
from pyramid.renderers import render, render_to_response

log = logging.getLogger(__name__)


class RestView(object):

    renderers = {}

    def __init__(self, request):
        self.request = request
        self.params = request.params
        self.url = request.route_url
        self.c = request.tmpl_context
        self.routes = self.request.matchdict

    def render_(self, *args, **kwargs):
        kwargs['request'] = self.request
        return render(*args, **kwargs)

    def render(self, *args, **kwargs):
        kwargs['request'] = self.request
        return render_to_response(*args, **kwargs)

    def index(self):
        raise HTTPNotImplemented()

    def new(self):
        raise HTTPNotImplemented()

    def create(self):
        raise HTTPNotImplemented()

    def view(self):
        raise HTTPNotImplemented()

    def edit(self):
        raise HTTPNotImplemented()

    def update(self):
        raise HTTPNotImplemented()

    def delete(self):
        raise HTTPNotImplemented()