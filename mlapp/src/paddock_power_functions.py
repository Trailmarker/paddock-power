# -*- coding: utf-8 -*-
from qgis.core import qgsfunction
from qgis.utils import plugins

from .spatial.schemas.feature_status import FeatureStatus
from .spatial.schemas.timeframe import Timeframe
from .spatial.schemas.waterpoint_type import WaterpointType
from .utils import PLUGIN_FOLDER, PLUGIN_NAME


def getCurrentProject():
    f"""Get the current {PLUGIN_NAME} Project."""
    return plugins[PLUGIN_FOLDER].project


@qgsfunction(args=0, group=PLUGIN_NAME)
def currentTimeframe(vals, *_):
    f"""Return the current {PLUGIN_NAME} Timeframe."""
    try:
        project = getCurrentProject()
        return project.currentTimeframe.name
    except BaseException:
        return None

@qgsfunction(args=1, group=PLUGIN_NAME)
def matchCurrentFeatureStatus(vals, *_):
    f"""Return True if a Feature Status matches the current {PLUGIN_NAME} Timeframe"""
    try:
        project = getCurrentProject()
        return project and vals[0] and project.currentTimeframe.matchFeatureStatus(FeatureStatus[vals[0]])
    except BaseException:
        return False


@qgsfunction(args=1, group=PLUGIN_NAME)
def matchCurrentTimeframe(vals, *_):
    f"""Return True if a Feature Status matches the current {PLUGIN_NAME} Timeframe."""
    try:
        project = getCurrentProject()
        return project and vals[0] and project.currentTimeframe == Timeframe[vals[0]]
    except BaseException:
        return False


@qgsfunction(args=3, group=PLUGIN_NAME)
def ifCurrentFeatureStatus(vals, *_):
    f"""Return True if a Feature Status matches the current {PLUGIN_NAME} Timeframe"""
    try:
        project = getCurrentProject()
        if project and vals[0] and project.currentTimeframe.matchFeatureStatus(FeatureStatus[vals[0]]):
            return vals[1]
        else:
            return vals[2]
    except BaseException:
        return vals[2]



@qgsfunction(args=3, group=PLUGIN_NAME)
def ifCurrentTimeframe(vals, *_):
    f"""Return True if a Feature Status matches the current {PLUGIN_NAME} Timeframe."""
    try:
        project = getCurrentProject()
        if project and vals[0] and project.currentTimeframe == Timeframe[vals[0]]:
            return vals[1]
        else:
            return vals[2]
    except BaseException:
        return vals[2]


@qgsfunction(args=0, group=PLUGIN_NAME)
def timeframeWaterpointColour(vals, *_):
    """Convert a Timeframe to a colour for a Waterpoint."""
    try:
        timeframe = getCurrentProject().currentTimeframe        
        
        if timeframe == Timeframe.Current:
            return "#026b7f"
        elif timeframe == Timeframe.Future:
            return "#83e9fd"
        elif timeframe == Timeframe.Drafted:
            return "#fadadd"
        elif timeframe == Timeframe.Undefined:
            return "#00000000"
        else:
            return None
    except BaseException:
        return None


@qgsfunction(args=0, group=PLUGIN_NAME)
def timeframeWaterpointForegroundColour(vals, *_):
    """Convert a Timeframe to a foreground colour for a Waterpoint."""
    try:
        timeframe = getCurrentProject().currentTimeframe

        if timeframe == Timeframe.Current:
            return "#ffffff"
        elif timeframe in [Timeframe.Drafted, Timeframe.Future]:
            return "#000000"
        elif timeframe == Timeframe.Undefined:
            return "#00000000"
        else:
            return None
    except BaseException:
        return None


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


PaddockPowerFunctions = [
    currentTimeframe,
    matchCurrentFeatureStatus,
    matchCurrentTimeframe,
    ifCurrentFeatureStatus,
    ifCurrentTimeframe,
    timeframeWaterpointColour,
    timeframeWaterpointForegroundColour,
    waterpointInitials
]
