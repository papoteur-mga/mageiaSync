#!/usr/bin/env python

from os import environ
from os.path import abspath, dirname, join
from setuptools import setup
from sys import path as sys_path

install_requires = [#"QtCore",
                    #"QtWidgets",
                    #"QtGui"
                    ]

data_files = [("share/applications/", ["share/applications/mageiasync.desktop"]),
              ("share/icons/hicolor/scalable/apps", ["share/icons/mageiasync.svg"])
              ]

srcdir = join(dirname(abspath(__file__)), "mageiasync/")
sys_path.insert(0, srcdir)

def readme():
    with open("README.rst") as f:
        return f.read()

setup(name="mageiasync",
      version="0.1",
      description="A frontend to rsync for Mageia usage",
      long_description=readme(),
      author="Papoteur",
      author_email="papoteur@mageialinux-online.org",
      url="https://github.com/papoteur-mga/mageiaSync",
      license="GPLv3",
      platforms=["Linux"],
#      keywords=['encoding', 'i18n', 'xml'],
      classifiers=["Development Status :: 5 - Production/Stable",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: GNU GENERAL PUBLIC LICENSE Version 3 (GPLv3)",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python :: 2.6",
                   "Programming Language :: Python :: 2.7",
                   "Programming Language :: Python :: 3.3",
                   "Programming Language :: Python :: 3.4",
                   "Topic :: Software Development :: Libraries :: Python Modules"],
      install_requires=install_requires,
      data_files=data_files,
      packages=["mageiasync"],
      py_modules=["mageiasync.mageiasync"],
      entry_points={"console_scripts": ["mageiasync=mageiasync.mageiasync:main"]}
      )
