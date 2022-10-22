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


class AddProjectFromExisting(QgsProcessingAlgorithm):
    NAME = 'AddProjectFromExisting'
    PROJECT_FILE_PARAM = 'ProjectFile'
    EXISTING_PROJECT_NAME_PARAM = 'ExistingProjectName'
    PROJECT_NAME_PARAM = 'ProjectName'
    NEW_PROJECT_OUTPUT = 'NewProject'

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFile(
            self.PROJECT_FILE_PARAM, 'Paddock Power Project File', fileFilter="QGS Project Files (*.qgz *.qgs)", optional=True))
        self.addParameter(QgsProcessingParameterString(
            self.EXISTING_PROJECT_NAME_PARAM, 'Existing Project Name', multiLine=False, defaultValue=None))
        self.addParameter(QgsProcessingParameterString(
            self.PROJECT_NAME_PARAM, 'Project Name', multiLine=False, defaultValue='New Project'))

    def processAlgorithm(self, parameters, context, model_feedback):
        results = {}
        outputs = {}

        existingProjectName = parameters[self.EXISTING_PROJECT_NAME_PARAM]
        projectName = parameters[self.PROJECT_NAME_PARAM]
        projectFilePath = parameters[self.PROJECT_FILE_PARAM]

        try:
            gpkgFile = resolveGeoPackageFile(projectFilePath)

            project = None
            if gpkgFile is not None:
                project = Project(gpkgFile)
                project.load()

                existingProject = project.getProject(existingProjectName)
                project = project.addProject(projectName)
                existingProject.copyTo(project)

            outputs[self.NEW_PROJECT_OUTPUT] = project
            results[self.NEW_PROJECT_OUTPUT] = project

        except Glitch as ppe:
            model_feedback.reportError(str(ppe))

        return results

    def name(self):
        return self.NAME

    def displayName(self):
        return 'Add Project From Existing Project'

    def icon(self):
        return QIcon(":/plugins/mlapp/images/new-project.png")

    def createInstance(self):
        return AddProjectFromExisting()
