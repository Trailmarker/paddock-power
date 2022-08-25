# -*- coding: utf-8 -*-
from os import path
from ..models.paddock_power_error import PaddockPowerError

import processing
from qgis.core import (QgsProcessingAlgorithm,
                       QgsProcessingParameterFile,
                       QgsProcessingParameterString)
from qgis.PyQt.QtGui import QIcon

from ..models.project import Project
from ..utils import resolveGeoPackageFile


class AddMilestoneFromExisting(QgsProcessingAlgorithm):
    NAME = 'AddMilestoneFromExisting'
    PROJECT_FILE_PARAM = 'ProjectFile'
    EXISTING_MILESTONE_NAME_PARAM = 'ExistingMilestoneName'
    MILESTONE_NAME_PARAM = 'MilestoneName'
    NEW_MILESTONE_OUTPUT = 'NewMilestone'

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFile(
            self.PROJECT_FILE_PARAM, 'Paddock Power Project File', fileFilter="QGS Project Files (*.qgz *.qgs)", optional=True))
        self.addParameter(QgsProcessingParameterString(
            self.EXISTING_MILESTONE_NAME_PARAM, 'Existing Milestone Name', multiLine=False, defaultValue=None))
        self.addParameter(QgsProcessingParameterString(
            self.MILESTONE_NAME_PARAM, 'Milestone Name', multiLine=False, defaultValue='New Milestone'))

    def processAlgorithm(self, parameters, context, model_feedback):
        results = {}
        outputs = {}

        existingMilestoneName = parameters[self.EXISTING_MILESTONE_NAME_PARAM]
        milestoneName = parameters[self.MILESTONE_NAME_PARAM]
        projectFilePath = parameters[self.PROJECT_FILE_PARAM]

        try:
            gpkgFile = resolveGeoPackageFile(projectFilePath)

            milestone = None
            if gpkgFile is not None:
                project = Project(gpkgFile)
                project.load()

                existingMilestone = project.getMilestone(existingMilestoneName)
                milestone = project.addMilestone(milestoneName)
                existingMilestone.copyTo(milestone)

            outputs[self.NEW_MILESTONE_OUTPUT] = milestone
            results[self.NEW_MILESTONE_OUTPUT] = milestone

        except PaddockPowerError as ppe:
            model_feedback.reportError(str(ppe))

        return results

    def name(self):
        return self.NAME

    def displayName(self):
        return 'Add Milestone From Existing Milestone'

    def icon(self):
        return QIcon(":/plugins/mlapp/images/new-milestone.png")

    def createInstance(self):
        return AddMilestoneFromExisting()
