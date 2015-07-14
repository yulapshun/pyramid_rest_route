import logging
import os
from pyramid.security import Everyone,\
    Allow, ALL_PERMISSIONS

log = logging.getLogger(__name__)


class PublicFactory(object):
    """
    ACE have smaller index in ACL have higher priority
    """
    __acl__ = None

    def __init__(self, request):
        log.debug('Init the PublicFactory')
        self.__acl__ = [
            (Allow, Everyone, ALL_PERMISSIONS),
        ]


def allowed_extension(*allowed):
    '''
    refs: http://zhuoqiang.me/a/restful-pyramid
    Custom predict checking if the the file extension
    of the request URI is in the allowed set.
    '''
    def predicate(info, request):
        log.debug(request.path)
        ext = os.path.splitext(request.path)[1]
        request.environ['path_extenstion'] = ext
        log.debug(ext)
        return ext in allowed

    return predicate


def add_rest_route(config, name, plural, cls, factory=PublicFactory,
        collections={}, members={},
        url_name=None, url_plural=None, exts=[''], include_view=True):
    if url_name is None:
        url_name = name
    if url_plural is None:
        url_plural = plural
    config.add_route('formatted_%s' % plural, '/%s.{ext}' % url_plural,
        factory=factory)
    config.add_route(plural, '/%s' % url_plural, factory=factory)
    config.add_route('formatted_new_%s' % name,
        '/%s/new.{ext}' % url_name, factory=factory)
    config.add_route('new_%s' % name, '/%s/new' % url_name,
        factory=factory)
    config.add_route('formatted_edit_%s' % name,
        '/%s/{id}/edit.{ext}' % url_name, factory=factory)
    config.add_route('edit_%s' % name, '/%s/{id}/edit' % url_name,
        factory=factory)
    config.add_route('formatted_%s' % name,
        '/%s/{id}.{ext}' % url_name, factory=factory)
    config.add_route('%s' % name, '/%s/{id}' % url_name,
        factory=factory)

    if include_view:
        config.add_view(cls, route_name=plural, permission='view',
            attr='index', request_method='GET', renderer=cls.renderers.get('index'))
        config.add_view(cls, route_name='formatted_%s' % plural,
            permission='view',
            attr='index', request_method='GET',
            custom_predicates=(allowed_extension(*exts),))

        config.add_view(cls, route_name=plural, permission='create',
            attr='create', request_method='POST',
            renderer=cls.renderers.get('create'))
        config.add_view(cls, route_name='formatted_%s' % plural,
            permission='create',
            attr='create', request_method='POST',
            custom_predicates=(allowed_extension(*exts),))

    for collection, permission in collections.items():
        route_name = '%s_%s' % (plural, collection)
        config.add_route(route_name,
            '/%s/%s' % (url_plural, collection),
            factory=factory)
        config.add_route('formatted_%s' % route_name,
            '/%s/%s.{ext}' % (url_plural, collection),
            factory=factory)

        if include_view:
            config.add_view(cls, route_name=route_name, permission=permission,
                attr=collection,
                renderer=cls.renderers.get(collection))
            config.add_view(cls, route_name='formatted_%s' % route_name,
                permission=permission,
                attr=collection,
                custom_predicates=(allowed_extension(*exts),))

    for member, permission in members.items():
        route_name = '%s_%s' % (member, name)
        config.add_route(route_name,
            '/%s/{id}/%s' % (url_name, member),
            factory=factory)
        config.add_route('formatted_%s' % route_name,
            '/%s/{id}/%s.{ext}' % (url_name, member),
            factory=factory)

        if include_view:
            config.add_view(cls, route_name=route_name,
                permission=permission,
                attr=member, renderer=cls.renderers.get(member))
            config.add_view(cls, route_name='formatted_%s' % route_name,
                permission=permission,
                attr=member,
                custom_predicates=(allowed_extension(*exts),))

    if include_view:
        config.add_view(cls, route_name='new_%s' % name, permission='create',
            attr='new', request_method='GET',
            renderer=cls.renderers.get('new'))
        config.add_view(cls, route_name='formatted_new_%s' % name,
            permission='create',
            attr='new', request_method='GET',
            custom_predicates=(allowed_extension(*exts),))
        config.add_view(cls, route_name='edit_%s' % name, permission='edit',
            attr='edit', request_method='GET',
            renderer=cls.renderers.get('edit'))
        config.add_view(cls, route_name='formatted_edit_%s' % name,
            permission='edit',
            attr='edit', request_method='GET',
            custom_predicates=(allowed_extension(*exts),))
        config.add_view(cls, route_name=name, permission='view',
            attr='view', request_method='GET',
            renderer=cls.renderers.get('view'))
        config.add_view(cls, route_name='formatted_%s' % name,
            permission='view',
            attr='view', request_method='GET')
        config.add_view(cls, route_name=name, permission='edit',
            attr='update', request_method='PUT',
            renderer=cls.renderers.get('update'))
        config.add_view(cls, route_name='formatted_%s' % name,
            permission='edit',
            attr='update', request_method='PUT',
            custom_predicates=(allowed_extension(*exts),))
        config.add_view(cls, route_name=name, permission='edit',
            attr='update', request_method='POST',
            renderer=cls.renderers.get('update'))
        config.add_view(cls, route_name='formatted_%s' % name,
            permission='edit',
            attr='update', request_method='POST',
            custom_predicates=(allowed_extension(*exts),))
        config.add_view(cls, route_name=name, permission='edit',
            attr='delete', request_method='DELETE',
            renderer=cls.renderers.get('delete'))
        config.add_view(cls, route_name='formatted_%s' % name,
            permission='edit',
            attr='delete', request_method='DELETE',
            custom_predicates=(allowed_extension(*exts),))
