import os
import re
from pyramid.response import Response
from pyramid.view import view_config


@view_config(
    route_name='home',
    renderer='templates/home.jinja2'
)
def home(request):
    settings = request.registry.settings
    
    dir_script = os.path.dirname(__file__)
    dir_app = os.path.abspath(os.path.join(dir_script, '..'))
    dir_albums = os.path.normpath(os.path.join(dir_app, settings['galdir.dir_albums']))

    if(os.path.isdir(dir_albums)):
        contents = os.listdir(dir_albums)

        # Process resulting directory list
        items = []
        for content in contents:
            if re.search(r'^\.', content) == None:
                if os.path.isdir(os.path.join(dir_albums, content)):
                    type = 'dir'
                else:
                    type = 'file'

                items.append({
                    'name': content,
                    'path': content,
                    'type': type,
                })

    return {'items': items}

@view_config(
    route_name = 'view',
    renderer='templates/home.jinja2'
)
def view(request):
    settings = request.registry.settings

    dir_script = os.path.dirname(__file__)
    dir_app = os.path.abspath(os.path.join(dir_script, '..'))
    dir_albums = os.path.normpath(os.path.join(
        dir_app, settings['galdir.dir_albums']))
    dir_view = os.path.normpath(os.path.join(
        dir_app, dir_albums, request.matchdict['path']))

    if os.path.isdir(dir_view):
        contents = os.listdir(dir_view)

        # Process resulting directory list
        items = []
        for content in contents:
            if re.search(r'^\.', content) == None:
                if os.path.isdir(os.path.join(dir_view, content)):
                    type = 'dir'
                else:
                    type = 'file'

                items.append({
                    'name': content,
                    'path': request.matchdict['path'] + '/' + content,
                    'type': type,
                })

    return {'items': items}