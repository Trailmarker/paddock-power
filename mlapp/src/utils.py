# -*- coding: utf-8 -*-
import os
from os import path

from qgis.PyQt.QtWidgets import QMessageBox
from qgis.core import Qgis, QgsMessageLog, QgsProject
from qgis.PyQt.QtCore import pyqtSignal


def guiInformation(message):
    """Show an info message box."""
    QMessageBox.information(None, "NAFI Burnt Areas Mapping", message)


def guiError(message):
    """Show an error message box."""
    QMessageBox.critical(None, "NAFI Burnt Areas Mapping", message)


def guiWarning(message):
    """Show a warning message box."""
    QMessageBox.warning(None, "NAFI Burnt Areas Mapping", message)


def guiConfirm(question="Are you sure?", title=None):
    """Show a confirmation dialog."""
    if title is None:
        title = "MLA Paddock Power"
    return QMessageBox.question(None, title, question, QMessageBox.Yes | QMessageBox.No, QMessageBox.No) == QMessageBox.Yes


def qgsDebug(message, tag="", level=Qgis.Info):
    """Print a debug message."""
    QgsMessageLog.logMessage(
        message, tag=tag, level=level)


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
        raise Exception(
            "Save the current QGIS session as your Paddock Power project before continuing.")
        return None
    return projectFilePath


def resolveGeoPackageFile(projectFilePath=None):
    """Get where the current Paddock Power GeoPackage should be."""
    if projectFilePath is None:
        projectFilePath = resolveProjectFile()
    if projectFilePath is None:
        return None
    return f"{path.splitext(projectFilePath)[0]}.gpkg"


def resolveStylePath(styleName):
    """Resolve the path of a style file packaged with the plugin."""
    relative = f"styles\\{styleName}.qml"
    return resolvePluginPath(relative)


# See https://stackoverflow.com/questions/28258875/how-to-obtain-the-set-of-all-signals-for-a-given-widget
def getSignals(source):
    """Get the signals of an object."""
    cls = source if isinstance(source, type) else type(source)
    signal = type(pyqtSignal())
    for subcls in cls.mro():
        clsname = f'{subcls.__module__}.{subcls.__name__}'
        for key, value in sorted(vars(subcls).items()):
            if isinstance(value, signal):
                print(f'{key} [{clsname}]')


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
