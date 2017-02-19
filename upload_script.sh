#!/bin/sh

source version.py
git add .
git commit -m "version update"
git push origin master
git tag $version
git push --tags origin master
python setup.py register -r pypi
python setup.py sdist upload -r pypi
