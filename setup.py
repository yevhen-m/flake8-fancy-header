"""
=====
setup
=====
"""

import os
import os.path
import setuptools
import sys

from setuptools import Command
from shutil import rmtree

install_requires = [
    "flake8 > 3.0.0",
]


here = os.path.abspath(os.path.dirname(__file__))


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    initialize_options = finalize_options = lambda self: None

    def run(self):
        try:
            print('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        print('Building Source and Wheel (universal) distribution…')
        os.system(f'{sys.executable} setup.py sdist bdist_wheel --universal')

        print('Uploading the package to PyPi via Twine…')
        os.system('twine upload dist/*')

        sys.exit()


setuptools.setup(
    name="flake8_fancy_header",
    license="MIT",
    version="0.1.0",
    description="check file has a fancy header at the top",
    author="yevhen-m",
    url="https://github.com/yevhen-m/flake8-fancy-header",
    packages=[
        "flake8_fancy_header",
    ],
    test_suite='tests',
    install_requires=install_requires,
    entry_points={
        'flake8.extension': [
            'S01 = flake8_fancy_header:FancyHeaderChecker',
        ],
    },
    classifiers=[
        "Framework :: Flake8",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
    ],
    cmdclass={
        'upload': UploadCommand,
    },
)
