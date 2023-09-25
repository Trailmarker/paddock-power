
# -*- coding: utf-8 -*-

# # from qgis.core import QgsApplication

# from paddock_power.dev import *

# # from .src.layers.features.persist_edits_task import PersistEditsTask

# wp = workspace().waterpointLayer
# wb = workspace().waterpointBufferLayer
# dw = workspace().wateredAreaLayer
# pl = workspace().paddockLandTypesLayer

# wpf = wp.getFeature(13)
# changeset = Edits.upsert(wpf)

# print(f"Changeset: {changeset}")

# wbChangeset = wb.deriveFeatures(changeset)

# changeset.editBefore(wbChangeset)
# changeset.persist()

# print(f"Changeset after deriving Waterpoint Buffers: {changeset}")

# dwChangeset = dw.deriveFeatures(changeset)

# changeset.editBefore(dwChangeset)
# changeset.persist()

# print(f"Changeset after deriving Watered Areas: {changeset}")

# plChangeset = pl.deriveFeatures(changeset)

# changeset.editBefore(plChangeset)
# changeset.persist()

# print(f"Changeset after deriving Paddock Land Types: {changeset}")


# # wp = first(workspace().waterpointLayer)

# # def editWaterpoint(w):
# #     qgsDebug(f"Waterpoint initial NEAR_GRAZING_RADIUS: {wp.NEAR_GRAZING_RADIUS}")
# #     w.NEAR_GRAZING_RADIUS = wp.NEAR_GRAZING_RADIUS / 2
# #     return Edits.upsert(wp)

# # task = PersistEditsTask(editWaterpoint, wp)

# # QgsApplication.taskManager().addTask(task)
