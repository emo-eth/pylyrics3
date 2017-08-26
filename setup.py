#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from setuptools import setup
from version import version

def load_version(path):
    with open(path) as fid:
        for line in fid:
            if line.startswith('version'):
                version = line.strip().split('=')[-1][1:-1]
                return version


version = load_version('version.py')

setup(
    name="pylyrics3",
    py_modules=['pylyrics3'],
    version=version,
    description="This is a package that downloads lyrics from LyricWiki.",
    author="James Wenzel",
    author_email="wenzel.james.r@gmail.com",
    url="https://github.com/jameswenzel/Lyric-Wiki-Scraper",
    download_url=('https://github.com/jameswenzel/pylyrics3/tarball/'
                  '{0}'.format(version)),
    license="Apache License, Version 2.0",
    keywords=["lyrics", "pylyrics", "lyricwiki", "music"],
    classifiers=[],
    install_requires=['beautifulsoup4>=4.4.1',
                      'requests>=2.2.1']
)
