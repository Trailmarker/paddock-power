# -*- coding: utf-8 -*-
from os import path
import sqlite3

from qgis.core import QgsRasterLayer

from ..models import Glitch, QtAbstractMeta, WorkspaceMixin
from ..utils import PLUGIN_NAME
from .map_layer_mixin import MapLayerMixin


class ElevationLayer(QgsRasterLayer, WorkspaceMixin, MapLayerMixin, metaclass=QtAbstractMeta):

    NAME = "Elevation Mapping"
    STYLE = "elevation"

    @staticmethod
    def _rasterGpkgUrl(workspaceFile, layerName):
        """Return a URL for a raster layer in a GeoPackage file."""
        # different from QgsVectorLayer GeoPackage URL format!
        return f"GPKG:{workspaceFile}:{layerName}"

    @classmethod
    def detectInGeoPackage(_, workspaceFile):
        """Find an elevation layer in a workspace GeoPackage."""
        try:
            if not path.exists(workspaceFile):
                return None

            db = sqlite3.connect(workspaceFile)
            cursor = db.cursor()
            cursor.execute(
                "SELECT table_name, data_type FROM gpkg_contents WHERE data_type = '2d-gridded-coverage'")
            grids = cursor.fetchall()

            if len(grids) == 0:
                return None
            elif len(grids) == 1:
                return grids[0][0]
            else:
                raise Glitch(
                    f"{PLUGIN_NAME} found multiple possible elevation layers in {workspaceFile}")
        except BaseException:
            return None

    def __init__(self, workspaceFile, layerName=None, *args, **kwargs):
        """Create a new elevation layer."""

        self._workspace = None

        # Route changes to this layer *through* the Paddock Power
        # workspace so other objects can respond
        self._blockWorkspaceConnnection = False

        layerName = layerName or ElevationLayer.NAME

        styleName = kwargs.pop("styleName", ElevationLayer.STYLE)

        # Note ths URL format is different from QgsVectorLayer!
        rasterUrl = ElevationLayer._rasterGpkgUrl(workspaceFile, layerName)
        QgsRasterLayer.__init__(self, rasterUrl, baseName=layerName)
        WorkspaceMixin.__init__(self)
        MapLayerMixin.__init__(self)

        self.applyNamedStyle(styleName)

        self.addInBackground()

    def __repr__(self):
        """Return a string representation of the Field."""
        return f"{type(self).__name__}(name={self.name()})"

    def __str__(self):
        """Convert the Field to a string representation."""
        return repr(self)
