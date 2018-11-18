
# =========================================
#       DEPS
# --------------------------------------

import sys
import os

from os import path

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

import rootpath

from rootpath.utils.banner import banner


# =========================================
#       FUNCTIONS
# --------------------------------------

def append(current_path = None, pattern = None):

    """
    Automatically adds current file's package root to Python load path (i.e. `sys.path`) unless already added.
    This makes it possible to always ensure module imports behave same no matter how the file is loaded.

    Examples:

        rootpath.append()
        rootpath.append(__file__)
        rootpath.append('./src')

    """
    project_root_path = rootpath.detect(current_path, pattern)

    try:
        if project_root_path != current_path:
            try:
                sys.path.remove(current_path)
            except:
                pass

        sys.path.index(project_root_path)

        return False, project_root_path

    except ValueError as error:
        sys.path.append(project_root_path)

        return True, project_root_path



# =========================================
#       MAIN
# --------------------------------------

if __name__ == '__main__':

    with banner(__file__):

        search_path = None
        result = append(search_path)

        print('append({0})\n\n  => {1}\n'.format(search_path, result))

        search_path = '.'
        result = append(search_path)

        print('append("{0}")\n\n  => {1}\n'.format(search_path, result))

        search_path = path.abspath(path.normpath(sys.argv.pop() or path.dirname(__file__)))
        result = append(search_path)

        print('append("{0}")\n\n  => {1}\n'.format(search_path, result))

