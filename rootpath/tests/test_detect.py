
# =========================================
#       IMPORTS
# --------------------------------------

import sys
import types

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

from rootpath.tests import helper

import rootpath


# =========================================
#       TEST
# --------------------------------------

class TestCase(helper.TestCase):

    def test__import(self):
        self.assertModule(rootpath)

        with self.assertNotRaises(Exception):
            from rootpath import detect

            self.assertTrue(callable(detect))

        with self.assertNotRaises(Exception):
            from rootpath import detect as detect_root

            self.assertTrue(callable(detect_root))

        with self.assertNotRaises(Exception):
            import rootpath.detect as detect

            self.assertTrue(callable(detect))

        with self.assertNotRaises(Exception):
            import rootpath.detect as detect_root

            self.assertTrue(callable(detect_root))

    def test_rootpath_detect_base(self):
        root_path = rootpath.detect()

        self.assertEqual(root_path, ROOT_PATH)

        root_path = rootpath.detect(helper.fixture_path('projects/null'))

        self.assertEqual(root_path, ROOT_PATH)

    def test_rootpath_detect_entry(self):
        foo_root_path = helper.fixture_path('projects/py-foo')

        root_path = rootpath.detect(helper.fixture_path('projects/py-foo'))

        self.assertEqual(root_path, foo_root_path)

        root_path = rootpath.detect(helper.fixture_path('projects/py-foo/'))

        self.assertEqual(root_path, foo_root_path)

        root_path = rootpath.detect(helper.fixture_path('projects/py-foo/foo'))

        self.assertEqual(root_path, foo_root_path)

        root_path = rootpath.detect(helper.fixture_path('projects/py-foo/foo/'))

        self.assertEqual(root_path, foo_root_path)

        root_path = rootpath.detect(helper.fixture_path('projects/py-foo'))

        self.assertEqual(root_path, foo_root_path)

        root_path = rootpath.detect(helper.fixture_path('projects/py-foo/'))

        self.assertEqual(root_path, foo_root_path)

        root_path = rootpath.detect(helper.fixture_path('projects/py-foo/foo'))

        self.assertEqual(root_path, foo_root_path)

        root_path = rootpath.detect(helper.fixture_path('projects/py-foo/foo/'))

        self.assertEqual(root_path, foo_root_path)

        root_path = rootpath.detect(helper.fixture_path('projects/py-foo/foo/utils'))

        self.assertEqual(root_path, foo_root_path)

        root_path = rootpath.detect(helper.fixture_path('projects/py-foo/foo/utils/'))

        self.assertEqual(root_path, foo_root_path)

    def test_rootpath_detect_entry_pattern(self):
        foo_root_path = helper.fixture_path('projects/py-foo')

        root_path = rootpath.detect(helper.fixture_path('projects/py-foo'), 'not_a_file')

        self.assertNotEqual(root_path, foo_root_path)

        root_path = rootpath.detect(helper.fixture_path('projects/py-foo/'), 'not_a_file')

        self.assertNotEqual(root_path, foo_root_path)

        root_path = rootpath.detect(helper.fixture_path('projects/py-foo/foo'), 'not_a_file')

        self.assertNotEqual(root_path, foo_root_path)

        root_path = rootpath.detect(helper.fixture_path('projects/py-foo/foo/'), 'not_a_file')

        self.assertNotEqual(root_path, foo_root_path)

        root_path = rootpath.detect(helper.fixture_path('projects/py-foo'), 'not_a_file')

        self.assertNotEqual(root_path, foo_root_path)

        root_path = rootpath.detect(helper.fixture_path('projects/py-foo/'), 'not_a_file')

        self.assertNotEqual(root_path, foo_root_path)

        root_path = rootpath.detect(helper.fixture_path('projects/py-foo/foo'), 'not_a_file')

        self.assertNotEqual(root_path, foo_root_path)

        root_path = rootpath.detect(helper.fixture_path('projects/py-foo/foo/'), 'not_a_file')

        self.assertNotEqual(root_path, foo_root_path)

        root_path = rootpath.detect(helper.fixture_path('projects/py-foo/foo/utils'), 'not_a_file')

        self.assertNotEqual(root_path, foo_root_path)

        root_path = rootpath.detect(helper.fixture_path('projects/py-foo/foo/utils/'), 'not_a_file')

        self.assertNotEqual(root_path, foo_root_path)

    def test_rootpath_detect_entry_nested(self):
        bar_root_path = helper.fixture_path('projects/py-foo/vendor/py-bar')

        root_path = rootpath.detect(helper.fixture_path('projects/py-foo/vendor/py-bar'))

        self.assertEqual(root_path, bar_root_path)

        root_path = rootpath.detect(helper.fixture_path('projects/py-foo/vendor/py-bar/'))

        self.assertEqual(root_path, bar_root_path)

        root_path = rootpath.detect(helper.fixture_path('projects/py-foo/vendor/py-bar/src'))

        self.assertEqual(root_path, bar_root_path)

        root_path = rootpath.detect(helper.fixture_path('projects/py-foo/vendor/py-bar/src/'))

        self.assertEqual(root_path, bar_root_path)

        root_path = rootpath.detect(helper.fixture_path('projects/py-foo/vendor/py-bar/src/utils'))

        self.assertEqual(root_path, bar_root_path)

        root_path = rootpath.detect(helper.fixture_path('projects/py-foo/vendor/py-bar/src/utils/'))

        self.assertEqual(root_path, bar_root_path)

    def test_rootpath_detect_entry_nested(self):
        bar_root_path = helper.fixture_path('projects/py-foo/vendor/py-bar')

        root_path = rootpath.detect(helper.fixture_path('projects/py-foo/vendor/py-bar'), 'not_a_file')

        self.assertEqual(root_path, None)

        root_path = rootpath.detect(helper.fixture_path('projects/py-foo/vendor/py-bar/'), 'not_a_file')

        self.assertEqual(root_path, None)

        root_path = rootpath.detect(helper.fixture_path('projects/py-foo/vendor/py-bar/src'), 'not_a_file')

        self.assertEqual(root_path, None)

        root_path = rootpath.detect(helper.fixture_path('projects/py-foo/vendor/py-bar/src/'), 'not_a_file')

        self.assertEqual(root_path, None)

        root_path = rootpath.detect(helper.fixture_path('projects/py-foo/vendor/py-bar/src/utils'), 'not_a_file')

        self.assertEqual(root_path, None)

        root_path = rootpath.detect(helper.fixture_path('projects/py-foo/vendor/py-bar/src/utils/'), 'not_a_file')

        self.assertEqual(root_path, None)


# =========================================
#       MAIN
# --------------------------------------

if __name__ == '__main__':
    helper.run(TestCase)
