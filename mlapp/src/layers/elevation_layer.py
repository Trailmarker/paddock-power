# -*- coding: utf-8 -*-
from os import path
import sqlite3

from qgis.core import QgsCoordinateReferenceSystem, QgsRasterLayer
import processing

from ..layers.interfaces import IImportableLayer
from ..models import Glitch, QtAbstractMeta, WorkspaceMixin
from ..utils import PLUGIN_NAME, PADDOCK_POWER_EPSG
from .map_layer_mixin import MapLayerMixin


class ElevationLayer(QgsRasterLayer, WorkspaceMixin, MapLayerMixin, IImportableLayer, metaclass=QtAbstractMeta):

    LAYER_NAME = "Elevation"
    STYLE = "elevation"

    @staticmethod
    def __getRasterGeoPackageUrl(workspaceFile, layerName):
        """Return a URL for a raster layer in a GeoPackage file."""
        # different from QgsVectorLayer GeoPackage URL format!
        return f"GPKG:{workspaceFile}:{layerName}"

    @classmethod
    def detectInStore(_, workspaceFile):
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

    @classmethod
    def importToStore(cls, workspaceFile, rasterLayer):
        """Import an elevation layer into a workspace GeoPackage."""

        # params = {
        #     "INPUT": rasterLayer.source(),
        #     "TARGET_CRS": QgsCoordinateReferenceSystem(f"EPSG:{PADDOCK_POWER_EPSG}"),
        #     "NODATA": None,
        #     "COPY_SUBDATASETS": False,
        #     "OPTIONS": f"APPEND_SUBDATASET=YES|RASTER_TABLE={cls.defaultName()}",
        #     "EXTRA": "",
        #     # Float32
        #     "DATA_TYPE": 6,
        #     "OUTPUT": workspaceFile
        # }

        # processing.run("gdal:translate", params)

        params = {
            "INPUT": rasterLayer.source(),
            "SOURCE_CRS": None,
            # "SOURCE_CRS": rasterLayer.crs(),
            "TARGET_CRS": QgsCoordinateReferenceSystem(f"EPSG:{PADDOCK_POWER_EPSG}"),
            "RESAMPLING": 1,
            "NODATA": None,
            "TARGET_RESOLUTION": None,
            "COPY_SUBDATASETS": False,
            "OPTIONS": f"APPEND_SUBDATASET=YES|OVERWRITE=YES|RASTER_TABLE={cls.defaultName()}",
            "EXTRA": "",
            # Float32
            "DATA_TYPE": 6,
            "TARGET_EXTENT": None,
            "TARGET_EXTENT_CRS": None,
            "MULTITHREADING": False,
            "EXTRA": "",
            "OUTPUT": workspaceFile
        }

        processing.run("gdal:warpreproject", params)

    def __init__(self, workspaceFile, layerName=None, *args, **kwargs):
        """Create a new elevation layer."""

        layerName = layerName or ElevationLayer.defaultName()
        styleName = kwargs.pop("styleName", ElevationLayer.defaultStyle())

        # Note ths URL format is different from QgsVectorLayer!
        rasterGeoPackageUrl = ElevationLayer.__getRasterGeoPackageUrl(workspaceFile, layerName)
        QgsRasterLayer.__init__(self, rasterGeoPackageUrl, baseName=layerName)
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
