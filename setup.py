#coding:utf-8
from setuptools import setup,find_packages

PACKAGE = "smysql"
NAME = "smysql"
DESCRIPTION = "simple mysql orm"
AUTHOR = "lovedboy"
AUTHOR_EMAIL = "lovedboy.tk@qq.com"
URL = "https://github.com/lovedboy/smysql"
VERSION = '0.1.2'

setup(
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
