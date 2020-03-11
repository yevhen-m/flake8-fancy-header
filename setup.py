"""
=====
setup
=====
"""

import setuptools

install_requires = [
    "flake8 > 3.0.0",
]

setuptools.setup(
    name="flake8_fancy_header",
    license="MIT",
    version="0.2.0",
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
)
