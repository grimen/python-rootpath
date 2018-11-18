
# =========================================
#       IMPORTS
# --------------------------------------

import sys
import os
import re
import six

from os import path, listdir

CURRENT_PATH = path.abspath(path.dirname(__file__))
ROOT_PATH = path.abspath(path.join(CURRENT_PATH, '..'))

try:
    try:
        sys.path.remove(CURRENT_PATH)
    except:
        pass

    sys.path.index(ROOT_PATH)

except ValueError:
    sys.path.insert(0, ROOT_PATH)

from rootpath.utils.banner import banner


# =========================================
#       CONSTANTS
# --------------------------------------

DEFAULT_PATH = '.'
DEFAULT_ROOT_FILENAME_MATCH_PATTERN = '.git|requirements.txt'


# =========================================
#       FUNCTIONS
# --------------------------------------

def detect(current_path = None, pattern = None):

    """
    Find project root path from specified file/directory path,
    based on common project root file pattern.

    Examples:

        from rootpath import rootpath

        rootpath.detect()
        rootpath.detect(__file__)
        rootpath.detect('./src')

    """

    current_path = current_path or os.getcwd()
    current_path = path.abspath(path.normpath(path.expanduser(current_path)))
    pattern = pattern or DEFAULT_ROOT_FILENAME_MATCH_PATTERN

    if not path.isdir(current_path):
        current_path = path.dirname(current_path)

    def find_root_path(current_path, pattern = None):
        if isinstance(pattern, six.string_types):
            pattern = re.compile(pattern)

        detecting = True

        while (detecting):
            file_names = listdir(current_path)
            no_more_files = len(file_names) <= 0

            if no_more_files:
                detecting = False

                return None

            project_root_files = filter(pattern.match, file_names)
            project_root_files = list(project_root_files)

            found_root = len(project_root_files) > 0

            if found_root:
                detecting = False

                return current_path

            if current_path == '/':
                return None

            current_path = path.abspath(path.join(current_path, '..'))

        return result

    root_path = find_root_path(current_path, pattern)

    return root_path


# =========================================
#       MAIN
# --------------------------------------

if __name__ == '__main__':

    with banner(__file__):

        search_path = None
        result = detect(search_path)

        print('detect({0})\n\n  => {1}\n'.format(search_path, detect(search_path)))

        search_path = '.'
        result = detect(search_path)

        print('detect("{0}")\n\n  => {1}\n'.format(search_path, detect(search_path)))

        search_path = path.abspath(path.normpath(sys.argv.pop() or path.dirname(__file__)))
        result = detect(search_path)

        print('detect("{0}")\n\n  => {1}\n'.format(search_path, detect(search_path)))
