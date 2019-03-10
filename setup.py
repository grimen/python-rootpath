

# =========================================
#       IMPORTS
# --------------------------------------

import os
import glob
import setuptools

# DISABLED/BUG: this line fails when `pip install palmtree` but works `pip install .`
# from palmtree import __version__


# =========================================
#       FUNCTIONS
# --------------------------------------

def find_data_files(data_file_patterns = [], root_path = None):
    root_path = root_path or os.path.abspath(os.path.dirname(__file__))
    data_file_dirs = []

    for root, dirs, files in os.walk(root_path):
        data_file_dirs.append(root)

    data_files = []

    for data_file_dir in data_file_dirs:
        files = []

        for data_file_pattern in data_file_patterns:
            files += glob.glob(os.path.join(data_file_dir, data_file_pattern))

        if not files:
            continue

        target = os.path.join(root_path, data_file_dir)

        data_files.append((target, files))

    return data_files

def get_readme():
    root_path = os.path.abspath(os.path.dirname(__file__))
    readme_file_path = os.path.join(root_path, 'README.md')

    with open(readme_file_path) as file:
        readme = file.read()

    return readme

def get_requirements():
    root_path = os.path.abspath(os.path.dirname(__file__))
    requirements_file_path = os.path.join(root_path, 'requirements.txt')

    with open(requirements_file_path) as file:
        requirements = [requirement.strip() for requirement in file.readlines()]
        requirements = filter(lambda requirement: len(requirement), requirements)
        requirements = list(requirements)

    return requirements

# import setuptools

# DISABLED/BUG: this line fails when `pip install rootpath` but works `pip install .`
# from rootpath import __version__

# =========================================
#       MAIN
# --------------------------------------

name = 'rootpath'
version = '0.1.1'
description = 'Python project/package root path detection.'
keywords = [
    'python',
    'utlity',
    'common',
    'root',
    'rootpath',
    'root-path',
    'detect',
    'autodetect',
    'auto-detect',
    'project-root',
    'project-root-path',
    'package-root',
    'package-root-path',
]

readme = get_readme()
requirements = get_requirements()
packages = setuptools.find_packages()
data_files = find_data_files(['*.*'], os.path.join(name, 'tests', '__fixtures__'))

config = {
    'name': name,
    'version': version,
    'description': (description),
    'keywords': keywords,
    'author': 'Jonas Grimfelt',
    'author_email': 'grimen@gmail.com',
    'url': 'https://github.com/grimen/python-{name}'.format(name = name),
    'download_url': 'https://github.com/grimen/python-{name}'.format(name = name),
    'project_urls': {
        'repository': 'https://github.com/grimen/python-{name}'.format(name = name),
        'bugs': 'https://github.com/grimen/python-{name}/issues'.format(name = name),
    },
    'license': 'MIT',

    'long_description': readme,
    'long_description_content_type': 'text/markdown',

    'classifiers': [
        'Topic :: Software Development :: Libraries',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],

    'packages': packages,
    'package_dir': {
        name: name,
    },
    'package_data': {
        '': [
            'MIT-LICENSE',
            'README.md',
        ],
        name: [
            '*.*',
        ],
    },
    'data_files': data_files,
    'include_package_data': True,
    'zip_safe': True,

    'install_requires': requirements,
    'setup_requires': [
        'setuptools_git >= 1.2',
    ],
}

setuptools.setup(**config)
