#!/bin/bash

# "default" profile directory
PLUGIN_PATH=/c/Users/tom.lynch/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins

rm -rf $PLUGIN_PATH/old
cp -r old $PLUGIN_PATH


