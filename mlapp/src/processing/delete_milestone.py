# -*- coding: utf-8 -*-
from os import path
from ..models.glitch import Glitch

import processing
from qgis.core import (QgsProcessingAlgorithm,
                       QgsProcessingParameterFile,
                       QgsProcessingParameterString)
from qgis.PyQt.QtGui import QIcon

from ..models.project import Project
from ..utils import resolveGeoPackageFile


class DeleteMilestone(QgsProcessingAlgorithm):
    NAME = 'DeleteMilestone'
    PROJECT_FILE_PARAM = 'ProjectFile'
    MILESTONE_NAME_PARAM = 'MilestoneName'

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFile(
            self.PROJECT_FILE_PARAM, 'Paddock Power Project File', fileFilter="QGS Project Files (*.qgz *.qgs)", optional=True))
        self.addParameter(QgsProcessingParameterString(
            self.MILESTONE_NAME_PARAM, 'Milestone Name', multiLine=False, defaultValue='New Milestone'))

    def processAlgorithm(self, parameters, context, model_feedback):
        results = {}

        milestoneName = parameters[self.MILESTONE_NAME_PARAM]
        projectFilePath = parameters[self.PROJECT_FILE_PARAM]

        try:
            gpkgFile = resolveGeoPackageFile(projectFilePath)

            if gpkgFile is not None:
                project = Project(gpkgFile)
                project.load()
                project.deleteMilestone(milestoneName)

        except Glitch as ppe:
            model_feedback.reportError(str(ppe))

        return results

    def name(self):
        return self.NAME

    def displayName(self):
        return 'Delete Milestone'

    def icon(self):
        return QIcon(":/plugins/mlapp/images/delete-milestone.png")

    def createInstance(self):
        return DeleteMilestone()
