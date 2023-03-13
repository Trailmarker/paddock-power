# -*- coding: utf-8 -*-
from time import sleep

from qgis.core import QgsTask

from ..utils import PLUGIN_NAME, qgsInfo


class SafeTaskCancelledException(Exception):
    """Custom exceptiopn type for emergency task management."""
    pass


class SafeTask(QgsTask):

    TASK_DELAY = 0.2

    def __init__(self, description):
        """Input is a closure over a FeatureAction handler for a given Feature."""
        super().__init__(description, flags=QgsTask.CanCancel | QgsTask.CancelWithoutPrompt)
        self._tasks = []

    def safeAddSubTask(self, task):
        assert isinstance(task, SafeTask)
        task.taskTerminated.connect(self.cancel)
        self.addSubTask(
            task, dependencies=self._tasks,
            subTaskDependency=QgsTask.SubTaskDependency.ParentDependsOnSubTask)
        self._tasks.append(task)

    def run(self):
        """Carry out a function that generates Feature edit operations, and persist the edits."""
        result = False
        
        try:
            result = self.safeRun()
        except SafeTaskCancelledException:
            qgsInfo(f"{PLUGIN_NAME} User successfully cancelled {self.description()}")
            result = False
        finally:
            sleep(self.TASK_DELAY)
        
        return result

    def safeRun(self):
        return True

    def finished(self, result):
        """Called when task completes (successfully or otherwise)."""
        sleep(self.TASK_DELAY)
        self.safeFinished(result)
        sleep(self.TASK_DELAY)

    def safeFinished(self, result):
        pass

    def raiseIfCancelled(self):
        if self.isCanceled():
            raise SafeTaskCancelledException()

    def cancel(self):
        qgsInfo(f"{PLUGIN_NAME} User started cancelling: {self.description()}")
        super().cancel()
        sleep(self.TASK_DELAY)
