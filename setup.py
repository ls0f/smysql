#coding:utf-8
from setuptools import setup,find_packages

PACKAGE = "smysql"
NAME = "smysql"
DESCRIPTION = "simple mysql orm"
AUTHOR = "ls0f"
AUTHOR_EMAIL = "ls0f@example.com"
URL = "https://github.com/ls0f/smysql"
VERSION = '0.2.9'

setup(
    install_requires=['pymysql'],
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="BSD",
    url=URL,
    include_package_data = True,
    packages = find_packages(),
    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    zip_safe=False,
)
