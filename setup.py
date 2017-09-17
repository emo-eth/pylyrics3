#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from setuptools import setup

version = '1.0.3'

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
