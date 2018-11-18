
# =========================================
#       DEPS
# --------------------------------------

import sys

from os import path

CURRENT_PATH = path.abspath(path.dirname(__file__))
ROOT_PATH = path.abspath(path.join(CURRENT_PATH, '..', '..'))

try:
    try:
        sys.path.remove(CURRENT_PATH)
    except:
        pass

    sys.path.index(ROOT_PATH)

except ValueError:
    sys.path.insert(0, ROOT_PATH)


# =========================================
#       CLASSES
# --------------------------------------

class Banner(object):

    def __init__(self, title, close = False, enabled = True):
        self.title = title
        self.close = close
        self.enabled = enabled

    def __enter__(self):
        if self.enabled:
            print('\n# =========================================')
            print('#       {0}'.format(self.title))
            print('# --------------------------------------\n')

    def __exit__(self, type, value, traceback):
        if self.enabled:
            if self.close:
                print('\n# --------------------------------------\n')

banner = Banner


# =========================================
#       MAIN
# --------------------------------------

if __name__ == '__main__':

    with Banner(__file__):
        print('foo\n')
