Pyramid helper to create restful route.

Using URL Dispatch and class base view.


At pyramid booststrap

```
def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include("pyramid_resources")
```

Registering route with `AppView`
```
    config.add_rest_route('app', 'apps', AppView,
        members={
            'basic': 'edit',
            'messaging': 'view',
            'admin': 'edit',
        },
        collections={
            'paid': 'admin',
        },
        factory=RootFactory)

```

A simple `AppView` implementation

```
class AppView(RestView):

    renderers = {
        'basic': '/app/basic.mako'
    }

    def basic(self):
        return {
            'location': 'Render at basic.mako'
        }

    @view_config(
        route_name='paid_app',
        renderer='json',
        custom_predicates=(allowed_extension(*['.json']),)
        permission='read')
    def paid(self):
        return {
            "message": "using json renderer on json extension"
        }


```
