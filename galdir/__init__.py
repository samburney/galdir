import os
from pyramid.config import Configurator


def main(global_config, **settings):
    config = Configurator(settings=settings)

    config.add_route('home', '/')
    config.add_route('view', '/view/{path:.*}')

    dir_script = os.path.dirname(__file__)
    dir_app = os.path.abspath(os.path.join(dir_script, '..'))
    dir_albums = os.path.normpath(os.path.join(dir_app, settings['galdir.dir_albums']))
    config.add_static_view('albums', dir_albums)

    config.scan('.views')
    return config.make_wsgi_app()
