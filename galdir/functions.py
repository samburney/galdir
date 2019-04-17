import os
import re

from PIL import Image

import logging
log = logging.getLogger(__name__)

# Split a file path into name/extension/options
def namesplit(path):
    namesplit = {}
    namesplit['file_fullpath'] = path

    # Break into path and filename
    path_parts = re.search(r'^(.*)\/(.*)', namesplit['file_fullpath'])
    if(path_parts != None):
        namesplit['file_dir'] = path_parts[1]
        namesplit['file_origname'] = path_parts[2]
    else:
        namesplit['file_dir'] = ''
        namesplit['file_origname'] = path

    # Break into filename and extension
    filename_parts = re.search(r'^(.*)\.(.*)', namesplit['file_origname'])
    namesplit['file_name'] = filename_parts[1]
    namesplit['file_ext'] = filename_parts[2]

    # Get file options, if they are set
    namesplit['file_options'] = False
    fileoption_parts = re.search(r'^(.*)-([x0-9]+)$', namesplit['file_name'])

    if fileoption_parts != None:
        namesplit['file_options'] = True
        namesplit['file_name'] = fileoption_parts[1]

        # Determine resize option(s)
        if re.search(r'x', fileoption_parts[2]):
            namesplit['file_newsize'] = [
                int(fileoption_parts[2].split('x')[0]),
                int(fileoption_parts[2].split('x')[1]),
            ]
        elif re.search(r'^[0-9]+$', fileoption_parts[2]):
            namesplit['file_newsize'] = [
                int(fileoption_parts[2]),
                int(fileoption_parts[2]),
            ]

    namesplit['file_cleanname'] = cleanname(namesplit['file_name'])

    return namesplit


# Get absolute path of albums dir
def get_albums_path(settings):
    dir_script = os.path.dirname(__file__)
    dir_app = os.path.abspath(os.path.join(dir_script, '..'))
    dir_albums = os.path.normpath(os.path.join(
        dir_app, settings['galdir.dir_albums']))

    return dir_albums

# Get requested file path info
def get_path_info(request):
    dir_albums = get_albums_path(request.registry.settings)

    if('path' in request.matchdict):
        path_request = request.matchdict['path']
        dir_view = os.path.normpath(os.path.join(dir_albums, path_request))
    else:
        path_request = ''
        dir_view = dir_albums

    path_info = {
        "dir_albums": dir_albums,
        "dir_view": dir_view,
        "path_request": path_request,
    }

    return path_info


# Resize image inside a box
def resize_crop(image, newsize):
    if(image.width > image.height):
        box = (
            int(image.width/2 - image.height/2),
            0,
            int(image.width/2 + image.height/2),
            image.height,
        )
    else:
        box = (
            0,
            int(image.height/2 - image.width/2),
            image.width,
            int(image.height/2 + image.width/2),
        )

    newimage = image \
        .crop(box) \
        .resize(newsize, resample=Image.BICUBIC)

    return newimage


# Split filter for jinja2
def split(value, index, char=','):
    return value.split(char)[index]


# Make a reproducible cleaned up filename
def cleanname(name):
    name = name.lower()                         # Lowercase
    name = re.sub(r'[^a-z0-9_]', '_', name)     # Replace all invalid characters with '_'
    name = re.sub(r'_[_]*', '_', name)          # Replace duplicate '_'
    name = name.strip('_')                      # Strip leading/trailing '_'

    return name
