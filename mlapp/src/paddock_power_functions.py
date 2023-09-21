# -*- coding: utf-8 -*-
from qgis.core import qgsfunction
from qgis.utils import plugins

from .layers.fields import FeatureStatus, Timeframe, WaterpointType
from .utils import PLUGIN_FOLDER, PLUGIN_NAME


def getWorkspace():
    f"""Get the current {PLUGIN_NAME} Workspace."""
    return plugins[PLUGIN_FOLDER].workspace


@qgsfunction(args=0, group=PLUGIN_NAME)
def currentTimeframe(vals, *_):
    f"""Return the current {PLUGIN_NAME} Timeframe."""
    try:
        workspace = getWorkspace()
        return workspace.timeframe.name
    except BaseException:
        return None


@qgsfunction(args=1, group=PLUGIN_NAME)
def matchCurrentTimeframeByFeatureStatus(vals, *_):
    f"""Return True if a Feature Status matches the current {PLUGIN_NAME} Timeframe"""
    try:
        workspace = getWorkspace()
        return workspace and vals[0] and workspace.timeframe.matchFeatureStatus(FeatureStatus[vals[0]])
    except BaseException:
        return False


@qgsfunction(args=1, group=PLUGIN_NAME)
def displayInCurrentTimeframeByFeatureStatus(vals, *_):
    f"""Return True if a Feature Status matches the current {PLUGIN_NAME} Timeframe"""
    try:
        workspace = getWorkspace()
        return workspace and vals[0] and workspace.timeframe.displayFeatureStatus(FeatureStatus[vals[0]])
    except BaseException:
        return False


@qgsfunction(args=1, group=PLUGIN_NAME)
def matchCurrentTimeframeByFeatureStatus(vals, *_):
    f"""Return True if a Feature Status matches the current {PLUGIN_NAME} Timeframe"""
    try:
        workspace = getWorkspace()
        return workspace and vals[0] and workspace.timeframe.matchFeatureStatus(FeatureStatus[vals[0]])
    except BaseException:
        return False


@qgsfunction(args=1, group=PLUGIN_NAME)
def matchCurrentTimeframe(vals, *_):
    f"""Return True if a Feature Timeframe matches the current {PLUGIN_NAME} Timeframe."""
    try:
        workspace = getWorkspace()
        return workspace and vals[0] and workspace.timeframe == Timeframe[vals[0]]
    except BaseException:
        return False


@qgsfunction(args=3, group=PLUGIN_NAME)
def ifCurrentFeatureStatus(vals, *_):
    f"""Return True if a Feature Status matches the current {PLUGIN_NAME} Timeframe"""
    try:
        workspace = getWorkspace()
        if workspace and vals[0] and workspace.timeframe.matchFeatureStatus(FeatureStatus[vals[0]]):
            return vals[1]
        else:
            return vals[2]
    except BaseException:
        return vals[2]


@qgsfunction(args=3, group=PLUGIN_NAME)
def ifCurrentTimeframe(vals, *_):
    f"""Return True if a Feature Status matches the current {PLUGIN_NAME} Timeframe."""
    try:
        workspace = getWorkspace()
        if workspace and vals[0] and workspace.timeframe == Timeframe[vals[0]]:
            return vals[1]
        else:
            return vals[2]
    except BaseException:
        return vals[2]


@qgsfunction(args=1, group=PLUGIN_NAME)
def waterpointInitials(vals, *_):
    """Convert a Waterpoint Type to initials for a Font Marker."""
    try:
        waterpointType = WaterpointType[vals[0]]

        if waterpointType == WaterpointType.Bore:
            return "B"
        elif waterpointType == WaterpointType.Dam:
            return "D"
        elif waterpointType == WaterpointType.Trough:
            return "T"
        elif waterpointType == WaterpointType.TurkeyNest:
            return "TN"
        elif waterpointType == WaterpointType.WaterTank:
            return "WT"
        elif waterpointType == WaterpointType.Waterhole:
            return "WH"
    except BaseException:
        return None


PaddockPowerFunctions = {
    "currentTimeframe": currentTimeframe,
    "matchCurrentTimeframeByFeatureStatus": matchCurrentTimeframeByFeatureStatus,
    "displayInCurrentTimeframeByFeatureStatus": displayInCurrentTimeframeByFeatureStatus,
    "matchCurrentTimeframe": matchCurrentTimeframe,
    "ifCurrentFeatureStatus": ifCurrentFeatureStatus,
    "ifCurrentTimeframe": ifCurrentTimeframe,
    "waterpointInitials": waterpointInitials
}
