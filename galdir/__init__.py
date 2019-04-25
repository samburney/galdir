import os

from flask import Flask
from galdir import functions

def create_app(test_config=None):
    app = Flask(__name__)

    # Default Config
    app.config.from_mapping(
        DEBUG = True,
        SECRET_KEY = 'not very secure',

        GALDIR_SITENAME = 'GalDir',
        #GALDIR_DIR_ALBUMS = 'albums',
        GALDIR_DIR_ALBUMS = 'C:\\Users\\sburn\\Pictures\\test-pictures-safe-to-delete',
        GALDIR_DIR_CACHE = 'cache',
        GALDIR_IMAGES_PERPAGE = 12,
    )

    # Jinja2 filters
    app.jinja_env.filters['split'] = functions.split

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # The views blueprint is the main logic of this app
    from . import views
    app.register_blueprint(views.bp)

    
    # Return app factory
    return app

#def main(global_config, **settings):
#    config = Configurator(settings=settings)
#
#    config.add_route('home', '/')
#    config.add_route('view', '/view/{path:.*}')
#    config.add_route('viewimage', '/viewimage/{path:.*}')
#    config.add_route('dirthumb', '/dirthumb/{path:.*}')
#
#    dir_albums = functions.get_albums_path(settings)
#    config.add_static_view('albums', dir_albums)
#    config.add_static_view('static', 'assets')
#
#    config.scan('.views')
#    return config.make_wsgi_app()
