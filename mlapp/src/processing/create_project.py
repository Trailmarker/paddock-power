# -*- coding: utf-8 -*-
import processing
from qgis.PyQt.QtGui import QIcon
from qgis.core import (QgsProcessing, QgsProcessingAlgorithm,
                       QgsProcessingParameterFile,
                       QgsProcessingParameterString)

from ..models.glitch import Glitch
from ..models.project import Project
from ..utils import resolveGeoPackageFile


class CreateProject(QgsProcessingAlgorithm):

    NAME = 'CreateProject'
    PROJECT_FILE_PARAM = 'QgisProjectFile'
    PROJECT_NAME_PARAM = 'ProjectName'
    NEW_PROJECT_OUTPUT = 'NewProject'

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFile(
            self.PROJECT_FILE_PARAM, 'QGIS Project File', fileFilter="QGS Project Files (*.qgz *.qgs)", optional=True))
        self.addParameter(QgsProcessingParameterString(
            self.PROJECT_NAME_PARAM, 'Project Name', multiLine=False, defaultValue='New Project'))

    def processAlgorithm(self, parameters, context, model_feedback):
        results = {}
        outputs = {}

        projectName = parameters[self.PROJECT_NAME_PARAM]
        projectFilePath = parameters[self.PROJECT_FILE_PARAM]

        try:
            gpkgFile = resolveGeoPackageFile(projectFilePath)

            project = None

            project = Project(gpkgFile)
            project.load()
            project = project.addProject(projectName)

            outputs[self.NEW_PROJECT_OUTPUT] = project
            results[self.NEW_PROJECT_OUTPUT] = project

        except Glitch as ppe:
            model_feedback.reportError(str(ppe))

        return results

    def name(self):
        return self.NAME

    def displayName(self):
        return 'Create Paddock Power Project'

    def icon(self):
        return QIcon(":/plugins/mlapp/images/new-paddock.png")

    def createInstance(self):
        return CreateProject()
