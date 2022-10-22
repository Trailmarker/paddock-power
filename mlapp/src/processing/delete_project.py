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


class DeleteProject(QgsProcessingAlgorithm):
    NAME = 'DeleteProject'
    PROJECT_FILE_PARAM = 'ProjectFile'
    PROJECT_NAME_PARAM = 'ProjectName'

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFile(
            self.PROJECT_FILE_PARAM, 'Paddock Power Project File', fileFilter="QGS Project Files (*.qgz *.qgs)", optional=True))
        self.addParameter(QgsProcessingParameterString(
            self.PROJECT_NAME_PARAM, 'Project Name', multiLine=False, defaultValue='New Project'))

    def processAlgorithm(self, parameters, context, model_feedback):
        results = {}

        projectName = parameters[self.PROJECT_NAME_PARAM]
        projectFilePath = parameters[self.PROJECT_FILE_PARAM]

        try:
            gpkgFile = resolveGeoPackageFile(projectFilePath)

            if gpkgFile is not None:
                project = Project(gpkgFile)
                project.load()
                project.deleteProject(projectName)

        except Glitch as ppe:
            model_feedback.reportError(str(ppe))

        return results

    def name(self):
        return self.NAME

    def displayName(self):
        return 'Delete Project'

    def icon(self):
        return QIcon(":/plugins/mlapp/images/delete-project.png")

    def createInstance(self):
        return DeleteProject()
