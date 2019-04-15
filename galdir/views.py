import os
import io
import re

from galdir import functions

from pyramid.response import Response
from pyramid.view import view_config

from PIL import Image

import logging
log = logging.getLogger(__name__)

@view_config(
    route_name='home',
    renderer='templates/home.jinja2'
)
def home(request):
    settings = request.registry.settings
    
    dir_script = os.path.dirname(__file__)
    dir_app = os.path.abspath(os.path.join(dir_script, '..'))
    dir_albums = os.path.normpath(os.path.join(dir_app, settings['galdir.dir_albums']))

    log.debug('Listing from ' + dir_albums)

    if(os.path.isdir(dir_albums)):
        contents = os.listdir(dir_albums)

        # Process resulting directory list
        items = []
        for content in contents:
            if re.search(r'^\.', content) == None:
                if os.path.isdir(os.path.join(dir_albums, content)):
                    type = 'dir'
                    items.append({
                        'name': content,
                        'path': content,
                        'type': type,
                    })
                else:
                    type = 'file'
                    items.append({
                        'name': content,
                        'path': content,
                        'type': type,
                        'namesplit': functions.namesplit(content),
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

    log.debug('Listing from ' + dir_view)

    if os.path.isdir(dir_view):
        contents = os.listdir(dir_view)

        # Process resulting directory list
        items = []
        for content in contents:
            if re.search(r'^\.', content) == None:
                if os.path.isdir(os.path.join(dir_view, content)):
                    type = 'dir'
                    items.append({
                        'name': content,
                        'path': request.matchdict['path'] + '/' + content,
                        'type': type,
                    })
                else:
                    type = 'file'
                    items.append({
                        'name': content,
                        'path': request.matchdict['path'] + '/' + content,
                        'type': type,
                        'namesplit': functions.namesplit(request.matchdict['path'] + '/' + content),
                    })

    return {'items': items}


@view_config(
    route_name = 'viewimage'
)
def viewimage(request):
    settings = request.registry.settings
    path_request = request.matchdict['path']

    dir_script = os.path.dirname(__file__)
    dir_app = os.path.abspath(os.path.join(dir_script, '..'))
    dir_albums = os.path.normpath(os.path.join(
        dir_app, settings['galdir.dir_albums']))

    image_namesplit = functions.namesplit(path_request) 
    log.debug(image_namesplit)

    dir_image = os.path.normpath(
        os.path.join(dir_app, dir_albums, image_namesplit['file_dir'], image_namesplit['file_name'] + '.' + image_namesplit['file_ext']))
    log.debug('Viewing from ' + dir_image)

    if os.path.isfile(dir_image):
        try:
            image = Image.open(dir_image)

            # Handle resize
            if image_namesplit['file_options']:
                file_newsize = image_namesplit['file_newsize'][0], image_namesplit['file_newsize'][1]
                image.thumbnail(file_newsize)

            with io.BytesIO() as thumb_bin:
                # Handle RGBA images
                if image.mode == 'RGBA':
                    image_mime = 'image/png'
                    image.save(thumb_bin, 'PNG')
                else:
                    image_mime = 'image/jpeg'
                    image.save(thumb_bin, 'JPEG')

                response = Response(
                    body = thumb_bin.getvalue(),
                    content_type = image_mime
                )

                return response

        except IOError:
            log.debug('Something broke.')

    else:
        return Response('File ' + dir_image + ' not found.')
