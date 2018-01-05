#!/bin/sh

git add .
git commit -m "version update"
git push origin master
git tag 1.0.3
git push --tags origin master
python setup.py register sdist upload -r pypi https://www.python.org/pypi
