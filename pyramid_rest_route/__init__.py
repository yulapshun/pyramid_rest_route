from .route import add_rest_route
from .view import RestView

def includeme(config):
    config.add_directive('add_rest_route', add_rest_route)
