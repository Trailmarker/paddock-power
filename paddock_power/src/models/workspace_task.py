# -*- coding: utf-8 -*-
from time import sleep, time

from qgis.core import QgsTask

from ..utils import PLUGIN_NAME, getSetting, qgsException, qgsInfo


class WorkspaceTaskCancelledException(Exception):
    """Custom exceptiopn type for emergency task management."""
    pass


class WorkspaceTask(QgsTask):

    TASK_DELAY = getSetting("taskDelay", default=1.0)

    def __init__(self, description, workspace):
        """Input is a closure over a FeatureAction handler for a given Feature."""
        super().__init__(description, flags=QgsTask.CanCancel | QgsTask.CancelWithoutPrompt)
        self.workspace = workspace
        self.startTime = time()
        self._tasks = []
        self._workspaceVisible = self.workspace.isVisible

    # Keeping things simple for now - we don't need subtasks (yet, maybe)
    # def safeAddSubTask(self, task):
    #     assert isinstance(task, WorkspaceTask)
    #     task.taskTerminated.connect(self.cancel)
    #     self.addSubTask(
    #         task, dependencies=self._tasks,
    #         subTaskDependency=QgsTask.SubTaskDependency.ParentDependsOnSubTask)
    #     self._tasks.append(task)

    def run(self):
        """Carry out a function that generates Feature edit operations, and persist the edits."""
        result = False
        try:
            self.workspace.lock()
            self.workspace.setVisible(False)
            result = self.safeRun()
        except WorkspaceTaskCancelledException:
            qgsInfo(f"{PLUGIN_NAME} User successfully cancelled '{self.description()}'")
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
            qgsInfo(f"{PLUGIN_NAME} '{self.description()}' completed in {(time() - self.startTime):.2f}s")
            self.workspace.unlock()
        except Exception:
            qgsException()
        finally:
            sleep(self.TASK_DELAY)
            self.workspace.setVisible(self._workspaceVisible)
            self.workspace.unlock()

    def safeFinished(self, result):
        pass

    def raiseIfCancelled(self):
        if self.isCanceled():
            raise WorkspaceTaskCancelledException()

    def cancel(self):
        qgsInfo(f"{PLUGIN_NAME} task cancellation requested: {self.description()}")
        super().cancel()
        sleep(self.TASK_DELAY)
