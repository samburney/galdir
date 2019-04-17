import os
import re
import math

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
        directories = []
        files = []
        for content in contents:
            # Add path delimiter if not the root directory
            if path_info['path_request'] != '':
                path_content = path_info['path_request'] + '/' + content
            else:
                path_content = content

            if not content.startswith('.'):
                if os.path.isdir(os.path.join(path_info['dir_view'], content)):
                    # Make sure this directory isn't empty
                    if len(os.listdir(os.path.join(path_info['dir_view'], content))) > 0:
                        path_type = 'dir'
                        directories.append({
                            'name': content,
                            'path': path_content,
                            'type': path_type,
                        })
                else:
                    path_type = 'file'

                    # Make sure this is an image, else skip it
                    try:
                        content_image = Image.open(os.path.join(path_info['dir_view'], content))
                        content_image.verify()

                        files.append({
                            'name': content,
                            'path': path_content,
                            'type': path_type,
                            'namesplit': functions.namesplit(path_content),
                        })

                    except IOError:
                        pass

    # Handle pagination
    pagination = {
        'perpage': int(request.registry.settings['galdir.images_perpage'])
    }
    try:
        pagination['number'] = int(request.params.getone('page'))
    except KeyError:
        pagination['number'] = 1
    
    pagination['start'] = (pagination['number'] - 1) * pagination['perpage']
    pagination['end'] = pagination['start'] + pagination['perpage']
    pagination['total'] = math.ceil(len(files) / pagination['perpage'])
    pagination['files_before'] = files[0:pagination['start']]
    pagination['files_after'] = files[pagination['end']:]

    # Return the page response
    response_data = {
        'directories': directories,
        'files': files[pagination['start']:pagination['end']],
        'pagination': pagination,
    }
    return response_data


@view_config(
    route_name = 'viewimage'
)
def viewimage(request):
    path_info = functions.get_path_info(request)
    image_namesplit = functions.namesplit(path_info['path_request'])
    image_cachename = image_namesplit['file_cleanname']

    # Handle filename options
    file_newsize = None
    if image_namesplit['file_options']:
        file_newsize = image_namesplit['file_newsize'][0], image_namesplit['file_newsize'][1]

        if image_namesplit['file_newsize'][0] == image_namesplit['file_newsize'][1]:
            image_cachename = image_cachename + '-' + \
                str(image_namesplit['file_newsize'][0])
        else:
            image_cachename = image_cachename + '-' + \
                str(image_namesplit['file_newsize'][0]) + 'x' + \
                str(image_namesplit['file_newsize'][1])

    # Build cachepath variable
    dir_cache = os.path.join(os.path.dirname(
                __file__), request.registry.settings['galdir.dir_cache'])
    image_cachepath = os.path.join(
        dir_cache, image_cachename + '.' + image_namesplit['file_ext'])

    # Determine image output format
    image_format = 'JPEG'
    image_mime = 'image/jpeg'
    if image_namesplit['file_ext'].lower() == 'png':
        image_format = 'PNG'
        image_mime = 'image/png'
    elif image_namesplit['file_ext'].lower() == 'gif':
        image_format = 'GIF'
        image_mime = 'image/gif'

    if not os.path.isfile(image_cachepath):
        dir_image = os.path.normpath(
            os.path.join(path_info['dir_albums'], image_namesplit['file_dir'], image_namesplit['file_name'] + '.' + image_namesplit['file_ext']))
        if os.path.isfile(dir_image):
            try:
                image = Image.open(dir_image)
                
                # Resize image if required
                if file_newsize:
                    image = functions.resize_crop(image, file_newsize)

                # Process file and output
                image.save(image_cachepath, format=image_format)


            except IOError:
                log.debug('Something broke.')
                return Response('Something broke.')

        else:
            return Response('File ' + dir_image + ' not found.')

    # Return cached file
    with open(image_cachepath, 'rb') as image_file:
        response = Response(
            content_type = image_mime,
            body = image_file.read()
        )
        return response


@view_config(
    route_name='dirthumb'
)
def dirthumb(request):
    path_info = functions.get_path_info(request)

    # Process directory name
    namesplit = functions.namesplit(path_info['path_request'])
    path_info['dir_view'] = os.path.normpath(os.path.join(path_info['dir_albums'], namesplit['file_dir'], namesplit['file_name']))
    path_info['path_request'] = namesplit['file_dir'] + '/' + namesplit['file_name']
    image_cachename = namesplit['file_cleanname'] + '_dir'

    # Use thumbnail size from file_options if specified, otherwise the default is 200x200
    # Handle filename options
    file_newsize = 200, 200
    if namesplit['file_options']:
        file_newsize = namesplit['file_newsize'][0], namesplit['file_newsize'][1]

        if namesplit['file_newsize'][0] == namesplit['file_newsize'][1]:
            image_cachename = image_cachename + '-' + \
                str(namesplit['file_newsize'][0])
        else:
            image_cachename = image_cachename + '-' + \
                str(namesplit['file_newsize'][0]) + 'x' + \
                str(namesplit['file_newsize'][1])

    # Determine colour mode to use
    thumb_mode = 'RGB'
    thumb_format = 'JPEG'
    thumb_background = (255, 255, 255)
    thumb_mime = 'image/jpeg'
    if namesplit['file_ext'].lower() == 'png':
        thumb_mode = 'RGBA'
        thumb_format = 'PNG'
        thumb_background = (255, 255, 255, 0)
        thumb_mime = 'image/png'
    elif namesplit['file_ext'].lower() == 'gif':
        thumb_format = 'GIF'
        thumb_mime = 'image/gif'
        thumb_background = (255, 255, 255, 0)

    # Build cachepath variable
    dir_cache = os.path.join(os.path.dirname(
        __file__), request.registry.settings['galdir.dir_cache'])
    image_cachepath = os.path.join(
        dir_cache, image_cachename + '.' + namesplit['file_ext'])

    if os.path.isdir(path_info['dir_view']):
        if not os.path.isfile(image_cachepath):
            with os.scandir(path_info['dir_view']) as entries:
                items = []
                for entry in entries:
                    if not entry.name.startswith('.'):
                        if entry.is_dir():
                            entry_path = os.path.join(os.path.dirname(
                                                    __file__), 'assets', 'images', 'directory-icon.png')
                        elif entry.is_file():
                            entry_path = os.path.join(path_info['dir_view'], entry.name)

                        # Make sure this is an image, else skip it
                        try:
                            entry_image = Image.open(entry_path)
                            entry_image.verify()
                            
                            items.append(entry_path)

                            if len(items) > 3:
                                break

                        except IOError:
                            pass

            # Create new image
            thumb_image = Image.new(thumb_mode, file_newsize, thumb_background)

            # Tile each item on new image
            for count, item in enumerate(items):
                item_newsize = (int(file_newsize[0] / 2), int(file_newsize[1] / 2))
                item_x = int((count % 2) * item_newsize[0])
                item_y = int(((count * item_newsize[1]) - item_x) / 2)

                # Make icons smaller and recentre
                if re.search(r'-icon\.png$', item):
                    item_newsize = (int((file_newsize[0] / 2) * 0.8), int((file_newsize[1] / 2) * 0.8))
                    item_x = item_x + int(((file_newsize[0] / 2) - item_newsize[0]) / 2)
                    item_y = item_y + int(((file_newsize[1] / 2) - item_newsize[1]) / 2)

                item_pos = (item_x, item_y)

                try:
                    item_image = functions.resize_crop(Image.open(item), item_newsize)

                    thumb_image.paste(item_image, item_pos)

                except IOError:
                    pass

            # Save cache image to disk
            if thumb_format == 'GIF':
                thumb_image.save(image_cachepath, thumb_format, transparency=0)
            else:
                thumb_image.save(image_cachepath, thumb_format)

        # Return cached file
        with open(image_cachepath, 'rb') as image_file:
            response = Response(
                content_type=thumb_mime,
                body=image_file.read()
            )
            return response

    else:
        response = 'Error: ' + path_info['dir_view'] + ' is not a directory.'
        log.debug(response)
        return Response(response)
