# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSignal, pyqtSlot

from ..spatial.features.feature import Feature
from ..spatial.features.fence import Fence
from ..spatial.features.paddock import Paddock
from ..spatial.features.pipeline import Pipeline
from ..widgets.fence_details.fence_selection import FenceSelection
from ..widgets.paddock_details.paddock_selection import PaddockSelection
from ..widgets.pipeline_details.pipeline_selection import PipelineSelection
from ..utils import qgsDebug, resolveGeoPackageFile, PLUGIN_NAME
from .glitch import Glitch
from .glitch_hook import GlitchHook
from .project import Project
from .singleton import Singleton


class State(GlitchHook, metaclass=Singleton):
    PLUGIN_NAME = "MLA Paddock Power"

    projectChanged = pyqtSignal(Project)
    projectDataChanged = pyqtSignal()
    selectedFeatureChanged = pyqtSignal(Feature)

    project = None

    def __init__(self):
        super().__init__()

        self.selectionsInitialised = False
        self.fenceSelection = None
        self.paddockSelection = None
        self.pipelineSelection = None

    @Glitch.glitchy(f"An exception occurred while trying to detect an {PLUGIN_NAME} project.")
    def detectProject(self):
        """Detect a Paddock Power project in the current QGIS project."""
        self.project = None
        gpkgFile = resolveGeoPackageFile()
        if gpkgFile is not None:
            self.project = Project(gpkgFile)
            self.projectChanged.emit(self.project)
            # qgsDebug(f"State.detectProject: detected project in {gpkgFile}")
            # else:
            #     qgsDebug(
            #         f"State.detectProject: no project detected in {gpkgFile}")
            #     return
        if self.project is not None:
            self.project.addToMap()

    def getProject(self):
        """Get the current Project."""
        return self.project

    def clearProject(self):
        """Clear the current Project, for example if the current QGIS project is closed."""
        if self.project is not None:
            self.project.removeFromMap()
            self.project = None
            self.projectChanged.emit(self.project)

    def setProject(self, project):
        """Set the current Project."""
        if not isinstance(project, Project):
            raise Glitch(
                "State.setProject: project is not a Project.")

        if self.project is not None:
            self.project.removeFromMap()

   
    def initSelections(self, canvas):
        """Initialize the selections."""
        self.selectionsInitialised = True

        self.paddockSelection = PaddockSelection(canvas)
        self.pipelineSelection = PipelineSelection(canvas)
        self.fenceSelection = FenceSelection(canvas)

        for selection in [self.paddockSelection,
                          self.pipelineSelection,
                          self.fenceSelection]:
            self.pluginUnloading.connect(lambda: selection.cleanUp())
            self.projectChanged.connect(
                lambda _: selection.clearSelectedFeature)

        self.selectedFeatureChanged.connect(lambda f:
                                            self.onSelectedFeatureChanged(f))

    @pyqtSlot()
    def onSelectedFeatureChanged(self, feature):
        """Handle a change in the selected feature."""
        if isinstance(feature, Fence):
            self.fenceSelection.setSelectedFeature(feature)
        elif isinstance(feature, Paddock):
            self.paddockSelection.setSelectedFeature(feature)
        elif isinstance(feature, Pipeline):
            self.pipelineSelection.setSelectedFeature(feature)

    @pyqtSlot()
    def onProjectChanged(self, project):
        """Handle a change in the current Paddock Power project."""
        pass


def connectStateListener(state, listener):
    """Connect a listener to the Paddock Power state."""
    if listener is not None:
        if hasattr(listener, "onProjectChanged") and callable(listener.onProjectChanged):
            state.projectChanged.connect(
                lambda p: listener.onProjectChanged(p))
        if hasattr(listener, "onSelectedFeatureChanged") and callable(listener.onSelectedFeatureChanged):
            state.selectedFeatureChanged.connect(
                lambda f: listener.onSelectedFeatureChanged(f))
        if hasattr(listener, "onProjectDataChanged") and callable(listener.onProjectDataChanged):
            state.projectDataChanged.connect(
                lambda: listener.onProjectDataChanged())
