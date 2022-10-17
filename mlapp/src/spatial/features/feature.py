# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QObject, pyqtSignal, pyqtSlot

from qgis.core import QgsFeature, QgsFields, QgsRectangle
from qgis.utils import iface

from ...models.paddock_power_error import PaddockPowerError
from ...utils import qgsDebug
from ..layers.edit_context import editAndCommit
from .feature_state_machine import FeatureStateMachine
from .schemas import FeatureSchema, addSchema

@addSchema(FeatureSchema)
class Feature(QObject):
    
    draft = pyqtSignal()
    plan = pyqtSignal()
    undoPlan = pyqtSignal()
    build = pyqtSignal()
    undoBuild = pyqtSignal()
    supersede = pyqtSignal()
    undoSupersede = pyqtSignal()
    archive = pyqtSignal()

    stateChanged = pyqtSignal()
    featuresProcessed = pyqtSignal(list)

    @classmethod
    def getWkbType(cls):
        """Return the Feature's wkbType."""
        raise NotImplementedError("Feature.getWkbType: must be implemented in subclass")

    @classmethod
    def checkSchema(cls, fieldsToCheck):
        """Check that an incoming schema contains this Feature's schema. Checks field names only."""
        return [field for field in cls.getSchema() if field.name() not in [f.name() for f in fieldsToCheck]]

    def __init__(self, featureLayer, existingFeature=None):
        """Create a new Feature."""
        super().__init__()

        # qgsDebug(f"Feature.__init__: creating instance of {self.__class__.__name__}")
        # qgsDebug(f"Feature.__init__: existingFeature.__class__.__name__ = {existingFeature.__class__.__name__}")

        # qgsDebug(f"{self.__class__.__name__}.__init__: existingFeature is a {existingFeature.__class__.__name__}")

        if isinstance(existingFeature, Feature):
            # Copy constructor
            qgsFeature = QgsFeature()
            qgsFeature.setAttributes(existingFeature._qgsFeature.attributes())
            qgsFeature.setGeometry(existingFeature._qgsFeature.geometry())
            qgsFeature.setId(-1)
            self.__init__(featureLayer, qgsFeature)
            return

        elif isinstance(existingFeature, QgsFeature):
            # qgsDebug(f"Feature.__init__: existingFeature.geometry().isEmpty() = {existingFeature.geometry().isEmpty()}")
            missingFields = self.checkSchema(existingFeature.fields().toList())
            if missingFields:
                raise PaddockPowerError(f"Nissing fields: {missingFields}")

            self._qgsFeature = existingFeature
        elif existingFeature is not None:
            raise PaddockPowerError(
                f"Feature.__init__: unexpected type {existingFeature.__class__.__name__} for provided existing feature data (should be a Feature subclass or QgsFeature)")
        else:
            # Build an empty QgsFeature and assign it
            fields = QgsFields()
            for field in self.getSchema():
                fields.append(field)
            self._qgsFeature = QgsFeature(fields)
            self.setId()

        self.featureLayer = featureLayer

        self._machine = FeatureStateMachine(self)

        self.stateChanged.connect(lambda: self.featureLayer.featureStateChanged.emit(self))

        self._machine.start()

    def __repr__(self):
        """Return a string representation of the Feature."""
        return f"Feature({repr(self._qgsFeature)})"

    def __str__(self):
        """Convert the Feature to a string representation."""
        return repr(self)

    def _debugStateMachine(self):
        """Debug the Feature's state machine."""
        return f"Feature._debugStateMachine: {self.__class__.__name__}: {self.id()}, {self.status}"

    def _upsert(self):
        """Add or update the Feature in the FeatureLayer."""
        if (self.id() >= 0):
            self.featureLayer.updateFeature(self)
        else:
            self.featureLayer.addFeature(self)

    def upsert(self):
        """If not currently editing, start editing, add or update the Feature in the FeatureLayer and commit the change.
           If currently editing, add or update the Feature and do not commit the change."""
        qgsDebug(f"{self.__class__.__name__} upsert")
        self.featureLayer.whileEditing(self._upsert)

    def upsertProcessedFeatures(self, features):
        """Add or update the provided features in the FeatureLayer."""
        qgsDebug(f"{self.__class__.__name__} upsertProcessedFeatures")

        featureLayers = set([f.featureLayer for f in features])

        with editAndCommit(featureLayers):
            for feature in features:
                feature.upsert()

    def delete(self):
        """Delete the Feature from the FeatureLayer."""
        self.featureLayer.deleteFeature(self)

    def zoomToFeature(self):
        """Zoom to the Feature."""
        featureExtent = QgsRectangle(self.geometry().boundingBox())
        featureExtent.scale(1.5)  # Expand by 50%
        iface.mapCanvas().setExtent(featureExtent)
        iface.mapCanvas().refresh()

    def id(self):
        """Return the Feature's fid."""
        return self._qgsFeature.id()

    def geometry(self):
        """Return the Feature's geometry."""
        return self._qgsFeature.geometry()

    def setId(self, fid=-1):
        """Set or the Feature's id."""
        self._qgsFeature.setId(fid)

    def setGeometry(self, geometry):
        """Set the Feature's geometry."""
        self._qgsFeature.setGeometry(geometry)

    @pyqtSlot()
    def recalculate(self):
        """Recalculate derived data about the Feature."""
        pass
