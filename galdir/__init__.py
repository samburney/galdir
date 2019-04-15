import os
from pyramid.config import Configurator

from galdir import functions

def main(global_config, **settings):
    config = Configurator(settings=settings)

    config.add_route('home', '/')
    config.add_route('view', '/view/{path:.*}')
    config.add_route('viewimage', '/viewimage/{path:.*}')
    config.add_route('dirthumb', '/dirthumb/{path:.*}')

    dir_albums = functions.get_albums_path(settings)
    config.add_static_view('albums', dir_albums)

    config.scan('.views')
    return config.make_wsgi_app()
