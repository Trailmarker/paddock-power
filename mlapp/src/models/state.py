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
from .milestone import Milestone
from .glitch import Glitch
from .glitch_hook import GlitchHook
from .project import Project
from .singleton import Singleton


class State(GlitchHook, metaclass=Singleton):
    PLUGIN_NAME = "MLA Paddock Power"

    milestoneChanged = pyqtSignal(Milestone)
    milestonesUpdated = pyqtSignal(dict)
    projectChanged = pyqtSignal(Project)
    selectedFeatureChanged = pyqtSignal(Feature)
    milestoneDataChanged = pyqtSignal()

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
        if self.project is None:
            gpkgFile = resolveGeoPackageFile()
            if gpkgFile is not None:
                milestones = Project.findMilestones(gpkgFile)
                if milestones:
                    qgsDebug(
                        f"State.detectProject: detected project with {len(milestones)} milestones in {gpkgFile}")
                    project = Project(gpkgFile)
                    self.setProject(project)
                    return
        else:
            self.refreshProject()

    def refreshProject(self):
        """Refresh the current project."""
        if self.project is not None:
            self.project.load()
            self.project.addToMap()

    def getProject(self):
        """Get the current Project."""
        return self.project

    def getMilestone(self):
        """Get the current Milestone."""
        if self.project is not None:
            return self.project.milestone
        else:
            return None

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

        self.project = project
        self.refreshProject()
        self.projectChanged.emit(self.project)

    def setMilestone(self, milestone):
        """Set the current Project."""
        if not isinstance(milestone, Milestone):
            raise Glitch(
                "State.setMilestone: milestone is not a Milestone.")

        if self.project is not None:
            self.project.setMilestone(milestone)
        else:
            raise Glitch(
                "State.setMilestone: there is no current Project.")

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
            self.milestoneChanged.connect(
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
        if self.project is not None:
            self.project.milestoneChanged.connect(
                lambda m: self.milestoneChanged.emit(m))
            self.project.milestonesUpdated.connect(
                lambda ms: self.milestonesUpdated.emit(ms))
            self.onMilestoneChanged(self.project.milestone)

    @pyqtSlot()
    def onMilestoneChanged(self, milestone):
        """Handle a change in the current Paddock Power milestone."""
        if self.project.milestone is not None:
            self.project.milestone.selectedFeatureChanged.connect(
                lambda f: self.selectedFeatureChanged.emit(f))


def connectStateListener(state, listener):
    """Connect a listener to the Paddock Power state."""
    if listener is not None:
        if hasattr(listener, "onMilestoneChanged") and callable(listener.onMilestoneChanged):
            state.milestoneChanged.connect(
                lambda m: listener.onMilestoneChanged(m))
        if hasattr(listener, "onMilestonesUpdated") and callable(listener.onMilestonesUpdated):
            state.milestonesUpdated.connect(
                lambda ms: listener.onMilestonesUpdated(ms))
        if hasattr(listener, "onProjectChanged") and callable(listener.onProjectChanged):
            state.projectChanged.connect(
                lambda p: listener.onProjectChanged(p))
        if hasattr(listener, "onSelectedFeatureChanged") and callable(listener.onSelectedFeatureChanged):
            state.selectedFeatureChanged.connect(
                lambda f: listener.onSelectedFeatureChanged(f))
        if hasattr(listener, "onMilestoneDataChanged") and callable(listener.onMilestoneDataChanged):
            state.milestoneDataChanged.connect(
                lambda: listener.onMilestoneDataChanged())
