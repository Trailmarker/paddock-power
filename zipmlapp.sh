#!/bin/bash

mkdir deployment

# get a clean copy of the current branch in a subdirectory `deployment`
git archive --verbose HEAD | tar -x -C deployment
cd deployment

# remove bare image files—these are encoded in resources.py anyway
cp mlapp/images/icon.png mlapp/icon.png
rm -rf mlapp/images

find . -name "*.qss" | xargs rm -f

# zip up the MLA Paddock Power plug-in directory only into a datestamped archive
7z a -r "../mlapp-$(date +'%Y%m%d').zip" mlapp
cd ..
rm -rf deployment


