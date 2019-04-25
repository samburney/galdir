import os

from flask import Flask, send_from_directory
from galdir import functions as f

def create_app(test_config=None):
    app = Flask(__name__)

    # Default Config
    app.config.from_mapping(
        DEBUG=True,
        SECRET_KEY='not very secure',

        GALDIR_SITENAME='GalDir',
        GALDIR_DIR_ALBUMS='albums',
        GALDIR_DIR_CACHE='cache',
        GALDIR_IMAGES_PERPAGE=12,
    )

    # Load config file, if it exists
    app.config.from_pyfile('config.py', silent=True)

    # Jinja2 config
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True
    
    # Custom Jinga2 filters
    @app.template_filter('split')
    def split(value, index, char=','):
        return value.split(char)[index]


    # Simulate a static directory for albums
    @app.route('/albums/<path:path>')
    def static_albums(path):
        dir_albums = f.get_albums_path()
        return send_from_directory(dir_albums, path)


    # The views blueprint is the main logic of this app
    from . import views
    app.register_blueprint(views.bp)


    # Return app factory
    return app
