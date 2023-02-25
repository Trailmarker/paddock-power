
from qgis.core import QgsApplication

from .dev import *

from .src.layers.features.persist_edits_task import PersistEditsTask

wp = first(workspace().waterpointLayer)

def editWaterpoint(w):
    qgsDebug(f"Waterpoint initial NEAR_GRAZING_RADIUS: {wp.NEAR_GRAZING_RADIUS}")
    w.NEAR_GRAZING_RADIUS = wp.NEAR_GRAZING_RADIUS / 2
    return Edits.upsert(wp)

task = PersistEditsTask(editWaterpoint, wp)

QgsApplication.taskManager().addTask(task)