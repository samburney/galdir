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
    return view(request)

@view_config(
    route_name = 'view',
    renderer='templates/home.jinja2'
)
def view(request):
    path_info = functions.get_path_info(request)

    if os.path.isdir(path_info['dir_view']):
        contents = os.listdir(path_info['dir_view'])

        # Process resulting directory list
        items = []
        for content in contents:
            # Add path delimiter if not the root directory
            if path_info['path_request'] != '':
                path_content = path_info['path_request'] + '/' + content
            else:
                path_content = content

            if re.search(r'^\.', content) == None:
                if os.path.isdir(os.path.join(path_info['dir_view'], content)):
                    path_type = 'dir'
                    items.append({
                        'name': content,
                        'path': path_content,
                        'type': path_type,
                    })
                else:
                    path_type = 'file'
                    items.append({
                        'name': content,
                        'path': path_content,
                        'type': path_type,
                        'namesplit': functions.namesplit(path_content),
                    })

    return {'items': items}


@view_config(
    route_name = 'viewimage'
)
def viewimage(request):
    path_info = functions.get_path_info(request)
    image_namesplit = functions.namesplit(path_info['path_request'])

    dir_image = os.path.normpath(
        os.path.join(path_info['dir_albums'], image_namesplit['file_dir'], image_namesplit['file_name'] + '.' + image_namesplit['file_ext']))

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


@view_config(
    route_name='dirthumb'
)
def dirthumb(request):

    return Response('test')
