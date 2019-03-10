
# `rootpath` [![PyPI version](https://badge.fury.io/py/rootpath.svg)](https://badge.fury.io/py/rootpath) [![Build Status](https://travis-ci.com/grimen/python-rootpath.svg?branch=master)](https://travis-ci.com/grimen/python-rootpath) [![Coverage Status](https://codecov.io/gh/grimen/python-rootpath/branch/master/graph/badge.svg)](https://codecov.io/gh/grimen/python-rootpath)

*Python project/package root path detection.*


## Introduction

Auto-magic project/package root path detection - from a child module file for Python libraries/projects.

It does this by detecting typical package/project root files/folders (e.g. `.git`, `requirements.txt`, etc.), but it can also be overriden easily if needed.

As a little bonus it exposes an optional helper for adding root path to the Python load path (`sys.path`) for resolving Python module import hell (which is terribly broken by design).


## Install

Install using **pip**:

```sh
pip install rootpath
```


## Use: Basic

Detect a project/package root path:

**1.** Assuming we have a **python** library/application project...

```
/home/me/projects
    └── py-foo
            └── foo
                └── utils
                    └── __init__.py
                    └── baz.py
                    └── say.py
                └── __init__.py
                └── bar.py
            README.md
            requirements.txt
            setup.py
```

`foo/bar.py` - top level package module

```python
import rootpath

def bar():
    path = rootpath.detect()

    assert path == '/home/me/projects/py-foo'

    print('---')
    print('FILE:', __file__)
    print('ROOT:', path)
    print('---')

if __name__ == '__main__':
    bar()
```

`foo/utils/baz.py` - nested level package module (dependency)

```python
import rootpath

def baz():
    path = rootpath.detect()

    assert path == '/home/me/projects/py-foo'

    print('---')
    print('FILE:', __file__)
    print('ROOT:', path)
    print('---')

if __name__ == '__main__':
    baz()
```

`foo/utils/say.py` - nested level package module (dependency)

```python
import rootpath

def say():
    print('---')
    print('SAY: {0}'.format(rootpath.detect()))
    print('---')

if __name__ == '__main__':
    say()
```

**2.** Let's run the files individually - they should both with successful assertions and output accurately detected root paths...

```sh
$ cd /home/me/projects/py-foo

$ python ./foo/bar.py

---
FILE: /home/me/projects/py-foo/foo/bar.py
ROOT: /home/me/projects/py-foo
---

$ python ./foo/utils/baz.py

---
FILE: /home/me/projects/py-foo/foo/utils/baz.py
ROOT: /home/me/projects/py-foo
---

$ python ./foo/utils/say.py

---
SAY: /home/me/projects/py-foo
---

```


## Use: Painless Python module imports

Using the above example code project as a reference, as and example to enable painless Python module imports:

**1.** Let's make use of the load path helper in the higher order modules...

`foo/bar.py`

```python
import rootpath

# 1. prepends root path to `sys.path`
rootpath.append()

# 2. will import correctly without errors no matter if imported/executed from same path or any other system path - which is not true for the native Python 3 relative import
import rootpath.utils.say as say

def bar():
    say()

if __name__ == '__main__':
    bar()
```

`foo/utils/baz.py`

```python
import rootpath

# 1. prepends root path to `sys.path`
rootpath.append()

# 2. will import correctly without errors no matter if imported/executed from same path or any other system path - which is not true for the native Python 3 relative import
import rootpath.utils.say as say

def baz():
    hello()

if __name__ == '__main__':
    baz()
```

**2.** Let's run the files individually - `say` module should be imported correctly without any errors from any module path namespace...

```sh
$ cd /home/me/projects/py-foo

$ python ./foo/bar.py

---
SAY: /home/me/projects/py-foo
---

$ python ./foo/utils/baz.py

---
SAY: /home/me/projects/py-foo
---

$ python ./foo/utils/say.py

---
SAY: /home/me/projects/py-foo
---

$ cd /home/me/projects/py-foo/foo

$ python ./bar.py
---
SAY: /home/me/projects/py-foo
---

$ python ./utils/baz.py
---
SAY: /home/me/projects/py-foo
---

$ python ./utils/say.py

---
SAY: /home/me/projects/py-foo
---

$ cd /home/me/projects/py-foo/foo/utils

$ python ./utils/baz.py

---
SAY: /home/me/projects/py-foo
---

$ python ./utils/say.py

---
SAY: /home/me/projects/py-foo
---
```


## About

This project was mainly initiated - in lack of well tested and reliable existing alternatives - to be used at our work at **[Markable.ai](https://markable.ai)** to have common code conventions between various programming environments where **Python** (research, CV, AI) is heavily used.


## License

Released under the MIT license.
