# -*- coding: utf-8 -*-
from collections.abc import Generator

import inspect
import json
import os
import random
import string
import traceback
from os import path

from qgis.PyQt.QtCore import QFile, pyqtSignal, pyqtBoundSignal
from qgis.PyQt.QtWidgets import QMessageBox

from qgis.core import Qgis, QgsMessageLog, QgsProject
from qgis.utils import iface

# Paddock Power data is held in the GDA2020 coordinate system
PADDOCK_POWER_EPSG = 7845

PLUGIN_NAME = "Paddock Power"
PLUGIN_FOLDER = "paddock_power"

# 16777215
MAX_QT_DIMENSION = (2 * 24 - 1)


def formatMessage(message):
    if isinstance(message, str):
        return message
    elif isinstance(message, list):
        if not message:
            return "An unknown error occurred."
        elif len(message) == 1:
            return message[0]
        return "".join([
            "<ul>",
            "".join(f"<li>{item}</li>" for item in message),
            "</ul>"
        ])


def qgsDebug(message, tag=PLUGIN_NAME, level=Qgis.Info):
    """Print a debug message."""
    if isinstance(message, str):
        QgsMessageLog.logMessage(message, tag, level)
    elif isinstance(message, list):
        for m in message:
            QgsMessageLog.logMessage(m, tag, level)


def qgsError(message):
    """Print a debug message."""
    qgsDebug(message, PLUGIN_NAME, Qgis.Critical)


def qgsInfo(message):
    """Print a debug message."""
    qgsDebug(message, PLUGIN_NAME, Qgis.Info)


def qgsException():
    qgsError(traceback.format_exc())


def guiInformation(message):
    """Show an info message box."""
    QMessageBox.information(None, f"{PLUGIN_NAME} | Information", formatMessage(message))
    # qgsDebug(message, level=Qgis.Info)


def guiError(message):
    """Show an error message box."""
    QMessageBox.critical(None, f"{PLUGIN_NAME} | Error", formatMessage(message))
    # qgsDebug(message, level=Qgis.Critical)


def guiWarning(message):
    """Show a warning message box."""
    QMessageBox.warning(None, f"{PLUGIN_NAME} | Warning", formatMessage(message))
    # qgsDebug(message, level=Qgis.Warning)


def guiConfirm(question="Are you sure?", title=None):
    """Show a confirmation dialog."""
    if title is None:
        title = PLUGIN_NAME
    return QMessageBox.question(None, title, question, QMessageBox.Yes |
                                QMessageBox.No, QMessageBox.No) == QMessageBox.Yes


def guiStatusBar(message):
    """Show a status bar message."""
    iface.mainWindow().statusBar().showMessage(message)


def guiStatusBarAndInfo(message):
    """Show a status bar message and an info message box."""
    guiStatusBar(message)
    qgsInfo(message)


def guiHelpNotYetImplemented():
    """Show a message saying this help section has not yet been implemented."""
    QMessageBox.information(None, f"{PLUGIN_NAME} | Help", "This help section has not yet been implemented.")


def resolvePluginPath(relative=None, base=None):
    """Resolve a relative path in the plug-in deployment directory."""
    if not base:
        base = path.dirname(os.path.realpath(__file__))
        # note this function will break if this code in src/utils.py is moved to a different directory
        base = path.normpath(path.join(base, os.pardir))
    return path.normpath(path.join(base, relative if relative else ""))


def getSetting(setting, default=None):
    f"""Retrieve a {PLUGIN_NAME} setting."""
    settingsFilePath = resolvePluginPath(f"{PLUGIN_FOLDER}.json")
    try:
        with open(settingsFilePath) as settingsFile:
            settings = json.load(settingsFile)
            return settings.get(setting, default)
    except BaseException:
        guiError("Error reading {PLUGIN_NAME} settings file at {settingsFilePath}")
        return default


def resolveProjectFile():
    """Get the current QGS project file path."""
    project = QgsProject.instance()
    projectFilePath = project.fileName()
    if projectFilePath is None or projectFilePath == '':
        return None
        # raise Exception(
        # "Save the current QGIS session as your Paddock Power workspace before continuing.")
    return projectFilePath


def resolveProjectPath(relative, projectFilePath=None):
    """Get a path relative to the current QGS project file."""
    projectFilePath = projectFilePath or resolveProjectFile()
    projectDir = path.dirname(projectFilePath)

    return path.normpath(path.join(projectDir, relative if relative else ""))


def resolveWorkspaceFile(projectFilePath=None):
    f"""Get where the current {PLUGIN_NAME} GeoPackage should be."""
    projectFilePath = projectFilePath or resolveProjectFile()
    return f"{path.splitext(projectFilePath)[0]}.gpkg" if projectFilePath else None


def resolveStylePath(styleName):
    """Resolve the path of a style file packaged with the plugin."""
    relative = path.join("styles", f"{styleName}.qml")
    return resolvePluginPath(relative)


def getComponentStyleSheet(componentFile):
    """Resolve the path of the component stylesheet file packaged with the plugin."""
    dir = path.dirname(componentFile)
    styleSheetFilename = path.join(dir, f"{path.splitext(path.basename(componentFile))[0]}.qss")
    styleSheetPath = path.relpath(styleSheetFilename, resolvePluginPath()).replace("\\", "/")
    resource = f":/plugins/{PLUGIN_FOLDER}/{styleSheetPath}"
    resourceFile = QFile(resource)
    if not resourceFile.exists():
        raise Exception(f"Stylesheet file {resource} not found.")
    resourceFile.open(QFile.ReadOnly | QFile.Text)
    return resourceFile.readAll().data().decode("utf-8")


def randomString(length=8):
    """Generate a random string of a specified length."""
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))


def ensureIterated(seq):
    """Ensure that a generator is iterated and returned as a list."""
    if isinstance(seq, Generator):
        return [item for item in seq]
    if isinstance(seq, tuple) or isinstance(seq, set):
        return list(seq)
    return seq


# See https://stackoverflow.com/questions/28258875/how-to-obtain-the-set-of-all-signals-for-a-given-widget
def getSignals(source):
    """Get the signals of an object, useful for debugging."""
    cls = source if isinstance(source, type) else type(source)
    signal = type(pyqtSignal())

    signals = []
    for subcls in cls.mro():
        clsname = f'{subcls.__module__}.{subcls.__name__}'

        for key, value in sorted(vars(subcls).items()):
            if isinstance(value, signal):
                signals.append((key, clsname, value))
    return signals


def getBoundSignals(obj):
    signal = pyqtBoundSignal
    return [(key, value) for (key, value) in inspect.getmembers(obj) if isinstance(value, signal)]
