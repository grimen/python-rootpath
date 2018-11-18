
import setuptools

# DISABLED/BUG: this line fails when `pip install rootpath` but works `pip install .`
# from rootpath import __version__

setuptools.setup(
    name = 'rootpath',
    version = '0.1.0',
    description = (
        'Python project/package root path detection.'
    ),
    long_description = open('README.md').read(),
    long_description_content_type = 'text/markdown',
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
    ],
    author = 'Jonas Grimfelt',
    author_email = 'grimen@gmail.com',
    url = 'https://github.com/grimen/python-rootpath',
    download_url = 'https://github.com/grimen/python-rootpath',
    project_urls = {
        'repository': 'https://github.com/grimen/python-rootpath',
        'bugs': 'https://github.com/grimen/python-rootpath/issues',
    },
    packages = setuptools.find_packages(),
    package_dir = {
        'rootpath': 'rootpath'
    },
    package_data = {
        '': [
            'MIT-LICENSE',
            'README.md',
        ],
        'rootpath': [
            '*.*',
        ]
    },
    license = 'MIT',
    classifiers = [
        'Topic :: Software Development :: Libraries',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    zip_safe = True,
)
