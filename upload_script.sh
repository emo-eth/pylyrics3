#!/bin/sh

git add .
git commit -m "version update"
git push origin master
git tag 1.0.2
git push --tags origin master
python setup.py register -r pypi
python setup.py sdist upload -r pypi
