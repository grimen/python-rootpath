
# =========================================
#       IMPORTS
# --------------------------------------

import sys

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


"""
Enable shortcut imports:

Examples for `detect`:

    `from rootpath import detect`

    `from rootpath import detect as detect_root`

    `import rootpath.detect as detect`

    `import rootpath.detect as detect_root`

Examples for `append`:

    `from rootpath import append`

    `from rootpath import append as append_root`

    `import rootpath.append as append`

    `import rootpath.append as append_root`

"""
from rootpath.detect import detect
from rootpath.append import append
