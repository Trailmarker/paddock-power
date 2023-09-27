#!/bin/bash

# "default" profile directory
PLUGIN_PATH=/c/Users/$(whoami)/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins

rm -rf $PLUGIN_PATH/paddock_power
cp -r paddock_power $PLUGIN_PATH


