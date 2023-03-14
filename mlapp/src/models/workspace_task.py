# -*- coding: utf-8 -*-
from time import sleep

from qgis.core import QgsTask

from ..utils import PLUGIN_NAME, qgsException, qgsInfo


class WorkspaceTaskCancelledException(Exception):
    """Custom exceptiopn type for emergency task management."""
    pass


class WorkspaceTask(QgsTask):

    TASK_DELAY = 0.3

    def __init__(self, description, workspace):
        """Input is a closure over a FeatureAction handler for a given Feature."""
        super().__init__(description, flags=QgsTask.CanCancel | QgsTask.CancelWithoutPrompt)
        self.workspace = workspace
        self._tasks = []

    def safeAddSubTask(self, task):
        assert isinstance(task, WorkspaceTask)
        task.taskTerminated.connect(self.cancel)
        self.addSubTask(
            task, dependencies=self._tasks,
            subTaskDependency=QgsTask.SubTaskDependency.ParentDependsOnSubTask)
        self._tasks.append(task)

    def run(self):
        """Carry out a function that generates Feature edit operations, and persist the edits."""
        result = False
        try:
            self.workspace.lock()
            result = self.safeRun()
        except WorkspaceTaskCancelledException:
            qgsInfo(f"{PLUGIN_NAME} User successfully cancelled {self.description()}")
            result = False
        except Exception:
            qgsException()
            result = False
        finally:
            sleep(self.TASK_DELAY)
        
        return result

    def safeRun(self):
        return True

    def finished(self, result):
        """Called when task completes (successfully or otherwise)."""
        try:
            sleep(self.TASK_DELAY)
            self.safeFinished(result)
            self.workspace.unlock()
        except Exception:
            qgsException()
        finally:
            sleep(self.TASK_DELAY)
        
    def safeFinished(self, result):
        pass

    def raiseIfCancelled(self):
        if self.isCanceled():
            raise WorkspaceTaskCancelledException()

    def cancel(self):
        qgsInfo(f"{PLUGIN_NAME} User requested to cancel: {self.description()}")
        super().cancel()
        sleep(self.TASK_DELAY)
