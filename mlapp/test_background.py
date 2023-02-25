
from qgis.core import QgsApplication

from .dev import *

global testTask
testTask = None


def testDeriveLayer(layer):
    testTask = DeriveEditsSingleTask(layer)
    testTask.taskCompleted.connect(lambda: qgsDebug(f"{testTask.description()} completed"))
    testTask.taskTerminated.connect(lambda: qgsDebug(f"{testTask.description()} terminated"))
    QgsApplication.taskManager().addTask(testTask)


def testDeriveWaterpointBuffers(): return testDeriveLayer(workspace().waterpointBufferLayer)
def testDeriveWateredAreas(): return testDeriveLayer(workspace().wateredAreaLayer)


def testDeriveSeveral():
    testTask = DeriveEditsTask([workspace().waterpointBufferLayer,
                                  workspace().wateredAreaLayer, workspace().paddockLandTypesLayer])
    testTask.taskCompleted.connect(lambda: qgsDebug(f"{testTask.description()} completed"))
    testTask.taskTerminated.connect(lambda: qgsDebug(f"{testTask.description()} terminated"))
    QgsApplication.taskManager().addTask(testTask)

