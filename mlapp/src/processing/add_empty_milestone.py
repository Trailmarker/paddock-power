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


class AddEmptyMilestone(QgsProcessingAlgorithm):
    NAME = 'AddMilestone'
    PROJECT_FILE_PARAM = 'ProjectFile'
    MILESTONE_NAME_PARAM = 'MilestoneName'
    NEW_MILESTONE_OUTPUT = 'NewMilestone'

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFile(
            self.PROJECT_FILE_PARAM, 'Paddock Power Project File', fileFilter="QGS Project Files (*.qgz *.qgs)", optional=True))
        self.addParameter(QgsProcessingParameterString(
            self.MILESTONE_NAME_PARAM, 'Milestone Name', multiLine=False, defaultValue='New Milestone'))

    def processAlgorithm(self, parameters, context, model_feedback):
        results = {}
        outputs = {}

        milestoneName = parameters[self.MILESTONE_NAME_PARAM]
        projectFilePath = parameters[self.PROJECT_FILE_PARAM]

        try:
            gpkgFile = resolveGeoPackageFile(projectFilePath)

            milestone = None
            if gpkgFile is not None:
                project = Project(gpkgFile)
                project.load()
                milestone = project.addMilestone(milestoneName)

            outputs[self.NEW_MILESTONE_OUTPUT] = milestone
            results[self.NEW_MILESTONE_OUTPUT] = milestone

        except PaddockPowerError as ppe:
            model_feedback.reportError(str(ppe))

        return results

    def name(self):
        return self.NAME

    def displayName(self):
        return 'Add Empty Milestone'

    def icon(self):
        return QIcon(":/plugins/mlapp/images/new-milestone.png")

    def createInstance(self):
        return AddEmptyMilestone()
