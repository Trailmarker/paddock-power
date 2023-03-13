# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QObject, pyqtSignal

from qgis.core import QgsApplication


class TaskHandle(QObject):

    taskCompleted = pyqtSignal()

    def __init__(self, taskType, lockObject=None):
        """Handle to contain everything needed to manage a pipeline of auto-cancelling tasks of the same type."""
        super().__init__()

        self._taskType = taskType
        self._taskId = -1
        self._task = None

    def run(self, *args, **kwargs):

        task = QgsApplication.taskManager().task(self._taskId)
        if task and task.isActive():
            task.cancel()
            self._taskId = -1

        self._task = self._taskType(*args, **kwargs)
        self._task.taskCompleted.connect(lambda: self.taskCompleted.emit())
        self._taskId = QgsApplication.taskManager().addTask(self._task)
