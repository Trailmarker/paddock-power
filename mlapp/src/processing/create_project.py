# -*- coding: utf-8 -*-
import processing
from qgis.PyQt.QtGui import QIcon
from qgis.core import (QgsProcessing, QgsProcessingAlgorithm,
                       QgsProcessingMultiStepFeedback,
                       QgsProcessingParameterFile,
                       QgsProcessingParameterString)

from ..models.project import Project
from ..utils import qgsDebug, resolveGeoPackageFile


class CreateProject(QgsProcessingAlgorithm):

    NAME = 'CreateProject'
    PROJECT_FILE_PARAM = 'QgisProjectFile'
    MILESTONE_NAME_PARAM = 'MilestoneName'
    NEW_MILESTONE_OUTPUT = 'NewMilestone'

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFile(
            self.PROJECT_FILE_PARAM, 'QGIS Project File', fileFilter="QGS Project Files (*.qgz *.qgs)", optional=True))
        self.addParameter(QgsProcessingParameterString(
            self.MILESTONE_NAME_PARAM, 'Milestone Name', multiLine=False, defaultValue='New Milestone'))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(1, model_feedback)
        results = {}
        outputs = {}

        milestoneName = parameters[self.MILESTONE_NAME_PARAM]
        projectFilePath = parameters[self.PROJECT_FILE_PARAM]

        gpkgFile = resolveGeoPackageFile(projectFilePath)

        milestone = None
        if gpkgFile is not None:
            project = Project(gpkgFile)
            project.load()
            milestone = project.addMilestone(milestoneName)

        outputs[self.NEW_MILESTONE_OUTPUT] = milestone
        results[self.NEW_MILESTONE_OUTPUT] = milestone

        return results

    def name(self):
        return self.NAME

    def displayName(self):
        return 'Create Paddock Power Project'

    def icon(self):
        return QIcon(":/plugins/mlapp/images/icon.png")

    def createInstance(self):
        return CreateProject()
