
# =========================================
#       IMPORTS
# --------------------------------------

import sys
import os
import inspect
import unittest
import json
import inspect
import pprint
import types
import six

import shutil, errno

from sys import version_info as python_version
from os import path, environ
from deepdiff import DeepDiff
from pygments import highlight, lexers, formatters
from termcolor import colored as color

try:
    # NOTE on `tox` (2/2): ran into issues with `tox` raising `ncurses` error, so disabling colors when running in `tox` for now
    from colour_runner.result import ColourTextTestResult
except:
    pass

CURRENT_PATH = path.abspath(path.dirname(__file__))
ROOT_PATH = path.abspath(os.getcwd())

PACKAGE_SOURCE_DIRECTORY = 'rootpath'
PACKAGE_SOURCE_PATH = path.join(ROOT_PATH, PACKAGE_SOURCE_DIRECTORY)

try:
    sys.path.index(PACKAGE_SOURCE_PATH)
except ValueError:
    sys.path.insert(0, PACKAGE_SOURCE_PATH)

TESTS_PATH = CURRENT_PATH
TESTS_ROOT_PATH = TESTS_PATH.replace('/__tests__', '')
FIXTURES_PATH = path.join(TESTS_PATH, '__fixtures__')

DEFAULT_TEST_ROOT_PATH = path.abspath(path.dirname(__file__))
DEFAULT_TEST_FILE_PATTERN = environ.get('TESTS_PATTERN', 'test_*.py')

PYTHON_VERSION = '.'.join([
    str(python_version.major),
    str(python_version.minor),
    str(python_version.micro),
])

print('# =========================================')
print('#       {0}'.format(__name__))
print('# --------------------------------------\n')

print('PYTHON_VERSION: {0}'.format(PYTHON_VERSION))
print('ROOT_PATH: {0}'.format(ROOT_PATH))
print('CURRENT_PATH: {0}'.format(CURRENT_PATH))
print('PACKAGE_SOURCE: {0}'.format(PACKAGE_SOURCE_DIRECTORY))
print('PACKAGE_SOURCE_PATH: {0}'.format(PACKAGE_SOURCE_PATH))
print('TESTS_PATH: {0}'.format(TESTS_PATH))
print('FIXTURES_PATH: {0}'.format(FIXTURES_PATH))
print('DEFAULT_TEST_ROOT_PATH: {0}'.format(DEFAULT_TEST_ROOT_PATH))
print('DEFAULT_TEST_FILE_PATTERN: {0}'.format(DEFAULT_TEST_FILE_PATTERN))

print('\n# --------------------------------------')


# =========================================
#       HELPERS
# --------------------------------------

# See: https://www.pythonsheets.com/notes/python-tests.html

def validate():
    is_system_package_path = ('.tox' not in str(TESTS_PATH)) and ('site-packages' in str(TESTS_PATH))

    if is_system_package_path:
        message = '\nERROR:\n\n' \
            'You are trying to run tests against a module loaded from a native system package path `{0}` instead of the actual project path `{1}`.\n' \
            'Either uninstall the package, or run tests in a virtual environment (e.g. `make test-ci`).\n'.format(TESTS_ROOT_PATH, ROOT_PATH)

        print(color(message, 'red'))

        return False

    return True

def run(test):
    if not validate():
        return

    loader = unittest.TestLoader()

    if isinstance(test, six.string_types):
        test_path = test

        if path.isfile(test_path):
            test_path = path.dirname(test_path)

        test = suite(path.abspath(test_path))

    if isinstance(test, unittest.TestSuite):
        _suite = test

    else:
        _suite = unittest.TestSuite()

        if isinstance(test, list):
            tests = test

        else:
            tests = [test]

        for test in tests:
            _suite.addTests(loader.loadTestsFromTestCase(test))

    print('')

    # NOTE on `tox` (2/2): ran into issues with `tox` raising `ncurses` error, so disabling colors when running in `tox` for now
    if 'ColourTextTestResult' in globals():
        result = unittest.runner.TextTestRunner(verbosity = 2, resultclass = ColourTextTestResult).run(_suite)
    else:
        result = unittest.runner.TextTestRunner(verbosity = 2).run(_suite)

    succesful = not result.wasSuccessful()
    exit_code = int(succesful)

    sys.exit(exit_code)

def suite(root = DEFAULT_TEST_ROOT_PATH, pattern = DEFAULT_TEST_FILE_PATTERN):
    root = root or DEFAULT_TEST_ROOT_PATH
    pattern = pattern or DEFAULT_TEST_FILE_PATTERN

    suite = unittest.TestSuite()

    for tests in unittest.defaultTestLoader.discover(root, pattern = pattern):
        for test in tests:
            try:
                suite.addTests(test)

            except Exception as error:
                raise ValueError('Failed to load tests - module import issue? {}'.format(tests))

    return suite

def load(root = DEFAULT_TEST_ROOT_PATH, pattern = DEFAULT_TEST_FILE_PATTERN):
    root = root or DEFAULT_TEST_ROOT_PATH
    pattern = pattern or DEFAULT_TEST_FILE_PATTERN

    unittest.defaultTestLoader.discover(root, pattern = pattern)

def deepdiff(a, b, exclude_types = None):
    exclude_types = exclude_types or []

    # FIXME: don't seem to cast correctly
    # a = compat_data.bytes2str(a)
    # b = compat_data.bytes2str(b)

    return DeepDiff(a, b, ignore_order = True, report_repetition = True, exclude_types = exclude_types)

def pretty(data):
    result = pprint.pformat(data, indent = 4, depth = None)
    result = highlight(result, lexers.PythonLexer(), formatters.TerminalFormatter())

    return result

def root_path(*args):
    return ROOT_PATH

def fixture_path(*args):
    args = list([FIXTURES_PATH]) + list(args)
    path_parts = filter(lambda value: value is not None, [FIXTURES_PATH] + args)

    return path.abspath(path.join(*path_parts))

def fixture_file(relative_file_path, *args, **kvargs):
    fixture_file_path = fixture_path(relative_file_path)

    return open(fixture_file_path, *args, **kvargs)

def fixture(relative_file_path, *args, **kvargs):
    return fixture_file(relative_file_path, *args, **kvargs)

def json_encode(data = None):
    return json.dumps(data, default = lambda x: repr(x)).replace(' ', '')

def copydir(src, dst):
    try:
        print('COPY DIR `{0}` => `{1}`'.format(src, dst))

        shutil.copytree(src, dst)

    except OSError as error: # python >2.5
        if error.errno == errno.ENOTDIR:
            shutil.copy(src, dst)

        else:
            raise

def makedir(path):
    try:
        print('CREATE DIR `{0}`'.format(path))

        os.makedirs(path)

    except OSError as error:  # Python >2.5
        if error.errno == errno.EEXIST and os.path.isdir(path):
            pass

        else:
            raise

def removedir(path):
    try:
        print('REMOVE DIR `{0}`'.format(path))

        shutil.rmtree(path)

    except OSError as error:  # Python >2.5
        pass

def assertModule(result, expression):
    is_string = isinstance(result.__file__, six.string_types)

    if not is_string:
        raise AssertionError('module path `{0}` expected to be a string - {1}'.format(result, expression and '- {0}'.format(expression) or ''))

    module_file_path = result.__file__

    is_source_file = (module_file_path.find('/{0}'.format(PACKAGE_SOURCE_DIRECTORY)) > -1) # ensure module is loaded from `src`

    if not is_source_file:
        raise AssertionError('module path `{0}` expected to include `{1}` {2}'.format(module_file_path, PACKAGE_SOURCE_DIRECTORY, expression and '- {0}'.format(expression) or ''))

    module_type = type(result)

    is_module = (module_type == types.ModuleType)

    if not is_module:
        raise AssertionError('module `{0}` expected to include `{1}` {2}'.format(module_file_path, PACKAGE_SOURCE_DIRECTORY, expression and '- {0}'.format(expression) or ''))

def assertDeepEqual(result, expected, expression = None, exclude_types = None):
    # HACK: `deepdiff` works differently on Python 2 vs Python 3 :'(
    # result = json.loads(json.dumps(result, default = lambda x: repr(x)))
    # expected = json.loads(json.dumps(expected, default = lambda x: repr(x)))

    diff = deepdiff(result, expected, exclude_types = exclude_types)

    if diff != {}:
        raise AssertionError('\n\n%s\nshould deep equal\n\n%s\ndiff:\n\n%s' % (pretty(result), pretty(expected), pretty(diff)))

    return True

def assertNotDeepEqual(result, expected, expression = None, exclude_types = None):
    # HACK: `deepdiff` works differently on Python 2 vs Python 3 :'(
    # result = json.loads(json.dumps(result, default = lambda x: repr(x)))
    # expected = json.loads(json.dumps(expected, default = lambda x: repr(x)))

    diff = deepdiff(result, expected, exclude_types = exclude_types)

    if diff == {}:
        raise AssertionError('\n\n%s\nshould deep equal\n\n%s\ndiff:\n\n%s' % (pretty(result), pretty(expected), pretty(diff)))

    return True

class assertNotRaises(unittest.TestCase):

    def __init__(self, exception, expression):
        self.exception = exception
        self.expression = expression

    def __enter__(self):
        if self.exception is None:
            try:
                self.expression()

            except:
                info = sys.exc_info()

                self.fail('%s raised' % repr(info[0]))

        else:
            self.assertRaises(self.exception, self.expression)

    def __exit__(self, type, value, traceback):
        pass

# See: https://stackoverflow.com/questions/4319825/python-unittest-opposite-of-assertraises
class TestCase(unittest.TestCase):

    maxDiff = None

    def assertNotRaises(self, exception, expression = None):
        return assertNotRaises(exception, expression)

    def assertDeepEqual(self, result, expected, expression = None, exclude_types = None):
        return assertDeepEqual(result, expected, expression)

    def assertNotDeepEqual(self, result, expected, expression = None, exclude_types = None):
        return assertNotDeepEqual(result, expected, expression)

    def assertModule(self, result, expression = None):
        return assertModule(result, expression)
