# -*- coding: utf-8 -*-
import os.path

from qgis.core import QgsApplication, QgsProject
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication, Qt
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction

# Initialize Qt resources from file resources.py
from .resources_rc import *

# Import the code for the dialog(s), dock widget(s) and processing provider
from .src.models.state import detectProject, getMilestone
from .src.paddock_view.paddock_view_dock_widget import PaddockViewDockWidget
from .src.provider import Provider
from .src.tools.fenceline_analysis.fenceline_analysis_tool import FencelineAnalysisTool
from .src.tools.split_paddock.split_paddock_tool import SplitPaddockTool
from .src.utils import guiError, qgsDebug


class PaddockPower:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface

        self.pluginPath = os.path.dirname(__file__)

        # Initialise locale
        locale = QSettings().value('locale/userLocale')[0:2]
        localePath = os.path.join(
            self.pluginPath,
            'i18n',
            'PaddockPower_{}.qm'.format(locale))

        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Paddock Power')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'PaddockPower')
        self.toolbar.setObjectName(u'PaddockPower')

        detectProject()
        QgsProject.instance().readProject.connect(detectProject)

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.firstStart = None

        self.pluginIsActive = False
        self.paddockView = None

    def tr(self, message):
        return QCoreApplication.translate('PaddockPower', message)

    def addAction(self,
                  icon,
                  text,
                  callback,
                  enabled=True,
                  addToMenu=False,
                  addToToolbar=True,
                  statusTip=None,
                  whatsThis=None,
                  parent=None):

        icon = QIcon(icon)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled)

        if statusTip is not None:
            action.setStatusTip(statusTip)

        if whatsThis is not None:
            action.setWhatsThis(whatsThis)

        if addToToolbar:
            self.toolbar.addAction(action)

        if addToMenu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        self.addAction(
            QIcon(':/plugins/mlapp/images/paddock.png'),
            text=self.tr(u'Paddock View'),
            callback=self.openPaddockView,
            parent=self.iface.mainWindow())

        self.addAction(
            QIcon(':/plugins/mlapp/images/split-paddock.png'),
            text=self.tr(u'Fenceline Analysis Tool'),
            callback=self.runFencelineAnalysis,
            parent=self.iface.mainWindow())

        self.addAction(
            QIcon(':/plugins/mlapp/images/split-paddock.png'),
            text=self.tr(u'Split Paddock Tool'),
            callback=self.runSplitPaddock,
            parent=self.iface.mainWindow())

        # Will be set False in run()
        self.firstStart = True

        # Register processing provider
        self.initProcessing()

    def initProcessing(self):
        """Init Processing provider for QGIS >= 3.8."""
        self.provider = Provider()
        QgsApplication.processingRegistry().addProvider(self.provider)

    def onClosePlugin(self):
        """Cleanup necessary items here when plugin dockwidget is closed"""
        # Disconnects
        self.paddockView.closingPlugin.disconnect(self.onClosePlugin)

        # Remove this statement if dockwidget is to remain
        # for reuse if plugin is reopened
        self.pluginIsActive = False

    def unload(self):
        """Removes the plugin menu item and icon from QGIS interface."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Paddock Power'),
                action)
            self.iface.removeToolBarIcon(action)
        # Remove the toolbar
        del self.toolbar

        # Remove processing provider
        QgsApplication.processingRegistry().removeProvider(self.provider)

    def openPaddockView(self):
        """Run method that loads and starts the plugin"""

        if not self.pluginIsActive:
            self.pluginIsActive = True

            # self.paddockView may not exist if:
            #    first run of plugin
            #    removed on close (see self.onClosePlugin method)
            if self.paddockView == None:
                self.paddockView = PaddockViewDockWidget()

            # Connect to provide cleanup on closing of self.paddockView
            self.paddockView.closingPlugin.connect(self.onClosePlugin)
            self.iface.addDockWidget(Qt.LeftDockWidgetArea, self.paddockView)
            self.paddockView.show()

    def runFencelineAnalysis(self):
        """Set FencelineAnalysisTool as a custom map tool."""
        milestone = getMilestone()

        if milestone is None:
            guiError("Please set the current Milestone before using the Fenceline Analysis tool.")
        else:
            milestone.setTool(FencelineAnalysisTool(milestone))

    def runSplitPaddock(self):
        """Set SplitPaddockTool as a custom map tool."""
        milestone = getMilestone()

        if milestone is None:
            guiError("Please set the current Milestone before using the Split Paddock tool.")
        else:
            milestone.setTool(SplitPaddockTool(milestone))

 
