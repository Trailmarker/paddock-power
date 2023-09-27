#!/bin/bash

mkdir deployment

# get a clean copy of the current branch in a subdirectory `deployment`
git archive --verbose HEAD | tar -x -C deployment
cd deployment

# remove bare image files—these are encoded in resources.py anyway
cp paddock_power/images/icon.png paddock_power/icon.png
rm -rf paddock_power/images

# remove unused scripts and bits and pieces
rm -rf paddock_power/uic.bat
rm -rf paddock_power/dev.py

find . -name "*.qss" | xargs rm -f

# zip up the Paddock Power plug-in directory only into a datestamped archive
# 7z a -r "../paddock_power-$(date +'%Y%m%d').zip" paddock_power
# cd ..
# rm -rf deployment


