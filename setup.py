"""
aws-flare
=========

AWS-FLARE is a general use library intended to alert on potential issues in aws primatives (security groups, ELBs, IAM, etc.)

:copyright: (c) 2015 by Netflix, see AUTHORS for more
:license: Apache, see LICENSE for more details.
"""
from __future__ import absolute_import
import sys
import os.path

from setuptools import setup

ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__)))

# When executing the setup.py, we need to be able to import ourselves, this
# means that we need to add the src/ directory to the sys.path.
sys.path.insert(0, ROOT)

about = {}
with open(os.path.join(ROOT, "aws_flare", "__about__.py")) as f:
    exec(f.read(), about)


install_requires = [
    'inflection==0.3.1',
    'marshmallow==2.9.0'
]

tests_require = [
]

dev_requires = [
    'flake8>=2.0,<3.0',
    'invoke',
    'twine'
]

setup(
    name=about["__title__"],
    version=about["__version__"],
    author=about["__author__"],
    author_email=about["__email__"],
    url=about["__uri__"],
    description=about["__summary__"],
    long_description=open(os.path.join(ROOT, 'README.md')).read(),
    packages=['aws_flare'],
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    extras_require={
        'tests': tests_require,
        'dev': dev_requires,
    },
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development',
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Natural Language :: English",
        "License :: OSI Approved :: Apache Software License"
    ]
)
