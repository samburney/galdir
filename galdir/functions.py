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

