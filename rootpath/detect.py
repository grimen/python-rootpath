
# =========================================
#       IMPORTS
# --------------------------------------

import sys
import os
import re
import six

from os import path, listdir


# =========================================
#       CONSTANTS
# --------------------------------------

DEFAULT_ROOT_FILENAME_MATCH_PATTERN = '.git|requirements.txt'


# =========================================
#       FUNCTIONS
# --------------------------------------

def detect(current_path = None, pattern = None):

    """
    Find project root path from specified file/directory path,
    based on common project root file pattern.

    Examples:

        import rootpath

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

        file_names = None

        while True:
            file_names = listdir(current_path)

            if not file_names:
                return None

            filtered_file_names_gen = filter(pattern.match, file_names)

            if list(filtered_file_names_gen):
                return current_path

            found_system_root = bool(current_path == path.sep)

            if found_system_root:
                return None

            current_path = path.dirname(current_path)

    return find_root_path(current_path, pattern)
