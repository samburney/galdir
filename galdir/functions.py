import os
import re

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
    filename_parts = re.search(r'^(.*)-([x0-9]+)$', namesplit['file_name'])

    if filename_parts != None:
        namesplit['file_options'] = True
        namesplit['file_name'] = filename_parts[1]

        # Determine resize option(s)
        if re.search(r'x', filename_parts[2]):
            namesplit['file_newsize'] = [
                int(filename_parts[2].split('x')[0]),
                int(filename_parts[2].split('x')[1]),
            ]
        elif re.search(r'^[0-9]+$', filename_parts[2]):
            namesplit['file_newsize'] = [
                int(filename_parts[2]),
                int(filename_parts[2]),
            ]

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
