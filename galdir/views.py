from pyramid.response import Response
from pyramid.view import view_config


@view_config(
    route_name='home',
    renderer='templates/home.jinja2'
)
def home(request):
    return {}


@view_config(route_name='hello')
def hello(request):
    return Response('<body>Go back <a href="/">home</a></body>')
