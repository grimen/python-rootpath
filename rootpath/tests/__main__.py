
# =========================================
#       IMPORTS
# --------------------------------------

import sys

from os import path

CURRENT_PATH = path.abspath(path.dirname(__file__))
ROOT_PATH = path.abspath(path.join(CURRENT_PATH, '..', '..'))

try:
    try:
        sys.path.remove(CURRENT_PATH)
    except:
        print('ERR #1')
        pass

    sys.path.index(ROOT_PATH)

except ValueError:
    print('ERR #2')
    sys.path.insert(0, ROOT_PATH)

print('sys.path', sys.path, CURRENT_PATH, ROOT_PATH)

from rootpath.tests import helper


# =========================================
#       MAIN
# --------------------------------------

helper.run(__file__)
