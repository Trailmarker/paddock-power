# -*- coding: utf-8 -*-
import inspect
import os
from os import path

from qgis.PyQt.QtWidgets import QMessageBox
from qgis.core import Qgis, QgsMessageLog, QgsProject
from qgis.PyQt.QtCore import pyqtSignal, pyqtBoundSignal


PLUGIN_NAME = "MLA Paddock Power"


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


def qgsInfo(message):
    """Print a debug message."""
    qgsDebug(message, PLUGIN_NAME, Qgis.Info)


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


def resolvePluginPath(relative, base=None):
    """Resolve a relative path in the plug-in deployment directory."""
    if not base:
        base = path.dirname(os.path.realpath(__file__))
        # note this function will break if this code in src/utils.py is moved to a different directory
        base = path.normpath(path.join(base, os.pardir))
    return path.normpath(path.join(base, relative))


def resolveProjectFile():
    """Get the current QGS project file path."""
    project = QgsProject.instance()
    projectFilePath = project.fileName()
    if projectFilePath is None or projectFilePath == '':
        return None
        # raise Exception(
        # "Save the current QGIS session as your Paddock Power project before continuing.")
    return projectFilePath


def resolveGeoPackageFile(projectFilePath=None):
    f"""Get where the current {PLUGIN_NAME} GeoPackage should be."""
    projectFilePath = projectFilePath or resolveProjectFile()
    return f"{path.splitext(projectFilePath)[0]}.gpkg" if projectFilePath else None


def resolveStylePath(styleName):
    """Resolve the path of a style file packaged with the plugin."""
    relative = f"styles\\{styleName}.qml"
    return resolvePluginPath(relative)


def resolveComponentStylesheet(componentType):
    """Resolve the path of the component stylesheet file packaged with the plugin."""
    relative = "stylesheets\\{componentType.__name__}.qss"
    return resolvePluginPath(relative)


# See https://stackoverflow.com/questions/28258875/how-to-obtain-the-set-of-all-signals-for-a-given-widget
def getSignals(source):
    """Get the signals of an object."""
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


def clearItem(item):
    """Fully delete a QWidget or QLayout and all of its children."""
    if hasattr(item, "layout"):
        if callable(item.layout):
            layout = item.layout()
            if layout is not None:
                for i in reversed(range(layout.count())):
                    clearItem(layout.itemAt(i))
                del layout

    if hasattr(item, "widget"):
        if callable(item.widget):
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                del widget


def staticinit(cls):
    if getattr(cls, "__staticinit__", None):
        cls.__staticinit__()
    return cls
