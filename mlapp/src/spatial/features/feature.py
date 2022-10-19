# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QObject, pyqtSignal, pyqtSlot

from qgis.core import QgsFeature, QgsFields, QgsRectangle
from qgis.utils import iface

from ...models.glitch import Glitch, glitchy
from ...utils import qgsDebug
from ..layers.edit_context import editAndCommit, editAndRollBack
from .feature_action import FeatureAction
from .feature_status import FeatureStatus
from .schemas import FeatureSchema


def addSchema(fields, wkbType=None):
    def addSchemaToFeature(cls):
        for field in fields:
            if field._propertyName is not None:
                field.addFieldProperty(cls)

        setattr(cls, "getSchema", classmethod(lambda _: fields))
        if wkbType is not None:
            setattr(cls, "getWkbType", classmethod(lambda _: wkbType))

        return cls
    return addSchemaToFeature


def actionHandler(action: FeatureAction):
    """Decorator that takes a method on a Feature, and returns a method that instead raises an exception if the
       Feature's current status means {action} is not permitted, and otherwise calls the original method, updates
       the Feature's status, and returns the result of the original method."""
    def makeActionHandler(handler, *a):
        def handlerWithTryAction(feature, *args, **kwargs):
            start = feature.status
            if feature.isPermitted(action):
                glitchMessage = f"An error happened trying to {action} a {feature}"
                result = ((glitchy(glitchMessage))(handler))(feature, *args, **kwargs)
                feature.doAction(action)
                return result
            else:
                raise Glitch(f"You can't {action} a {feature}, because it is {feature.status}")
        return handlerWithTryAction
    return makeActionHandler


def persistEdits(method):
    """Decorator that takes a method returning a tuple (upserts, deletes) of edits to persist,
       and returns a method that instead persists the edits and returns None."""
    def methodWithPersistEdits(feature, *args, **kwargs):
        upserts, deletes = method(feature, *args, **kwargs)

        qgsDebug(f"Persisting edits: upserts={repr(upserts)}, deletes={repr(deletes)}")

        layers = set([f.featureLayer for f in upserts + deletes])
        with editAndCommit(*layers):
            for feature in upserts:
                feature.upsert()
            for feature in deletes:
                feature.delete()
        return None
    return methodWithPersistEdits


def gatherEdits(edits=None, otherEdits=None):
    edits = edits or ([], [])
    otherEdits = otherEdits or ([], [])
    return (edits[0] + otherEdits[0], edits[1] + otherEdits[1])


def upserts(feature, otherEdits=None):
    return gatherEdits(otherEdits, ([feature], []))


def deletes(feature, otherEdits=None):
    return gatherEdits(otherEdits, ([], [feature]))


@addSchema(FeatureSchema)
class Feature(QObject):

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

        if not existingFeature:
            # Build an empty QgsFeature and wrap it up
            fields = QgsFields()
            for field in self.getSchema():
                fields.append(field)
            self._qgsFeature = QgsFeature(fields)
            self.clearId()

        elif isinstance(existingFeature, Feature):
            # Copy constructor for Feature and subclasses

            # Incoming Feature must have compatible schema
            missingFields = self.checkSchema(existingFeature.getSchema())
            if missingFields:
                raise Glitch(f"{self.__class__.name__}: incoming Feature has missing fields: {missingFields}")

            # First create an empty Feature with the correct schema
            self.__init__(featureLayer)

            # Then set all attributes and geometry
            self._qgsFeature.setAttributes(existingFeature._qgsFeature.attributes())
            self._qgsFeature.setGeometry(existingFeature._qgsFeature.geometry())

            # Clear FID so that it will be created on upsert
            self.clearId()
            return

        elif isinstance(existingFeature, QgsFeature):
            # Incoming QgsFeature must have the correct schema
            missingFields = self.checkSchema(existingFeature.fields().toList())
            if missingFields:
                raise Glitch(f"{self.__class__.name__} incoming QgsFeature has missing fields: {missingFields}")

            self._qgsFeature = existingFeature
  
        elif existingFeature is not None:
            # What?
            raise Glitch(
                f"Feature.__init__: unexpected type {existingFeature.__class__.__name__} for provided existing feature data (should be a Feature subclass or QgsFeature)")
  
        self.featureLayer = featureLayer

    def __repr__(self):
        """Return a string representation of the Feature."""
        return f"{self.__class__.__name__}(id={self.id}, name='{self.name}', status={self.status})"

    def __str__(self):
        """Convert the Feature to a string representation."""
        return repr(self)

    # State machine interface
    __TRANSITIONS = {
        (FeatureStatus.Undefined, FeatureAction.draft): FeatureStatus.Drafted,
        (FeatureStatus.Undefined, FeatureAction.plan): FeatureStatus.Planned,

        (FeatureStatus.Drafted, FeatureAction.trash): FeatureStatus.Undefined,
        (FeatureStatus.Drafted, FeatureAction.plan): FeatureStatus.Planned,
        (FeatureStatus.Drafted, FeatureAction.archive): FeatureStatus.Archived,

        (FeatureStatus.Planned, FeatureAction.undoPlan): FeatureStatus.Drafted,
        (FeatureStatus.Planned, FeatureAction.build): FeatureStatus.Built,
        (FeatureStatus.Planned, FeatureAction.supersede): FeatureStatus.PlannedSuperseded,
        (FeatureStatus.Planned, FeatureAction.archive): FeatureStatus.Archived,

        (FeatureStatus.Built, FeatureAction.undoBuild): FeatureStatus.Planned,
        (FeatureStatus.Built, FeatureAction.supersede): FeatureStatus.BuiltSuperseded,
        (FeatureStatus.Built, FeatureAction.archive): FeatureStatus.Archived,

        (FeatureStatus.PlannedSuperseded, FeatureAction.undoSupersede): FeatureStatus.Planned,
        (FeatureStatus.PlannedSuperseded, FeatureAction.archive): FeatureStatus.Archived,

        (FeatureStatus.BuiltSuperseded, FeatureAction.undoSupersede): FeatureStatus.Built,
        (FeatureStatus.BuiltSuperseded, FeatureAction.archive): FeatureStatus.Archived,
    }

    def isPermitted(self, action: FeatureAction):
        """Return True if the action is enabled for the current status."""
        return (self.status, action) in Feature.__TRANSITIONS

    def allPermitted(self):
        """Return a list of all enabled actions for the current status."""
        return [action for (status, action) in Feature.__TRANSITIONS if status == self.status]

    def doAction(self, action: FeatureAction):
        if self.isPermitted(action):
            self.status = Feature.__TRANSITIONS[(self.status, action)]
        else:
            raise Glitch(f"An error happened trying to {action} a {self}")

    def upsert(self):
        """Add or update the Feature in the FeatureLayer."""
        if (self.id >= 0):
            self.featureLayer.updateFeature(self)
        else:
            self.featureLayer.addFeature(self)

    def delete(self):
        """Delete the Feature from the FeatureLayer."""
        self.featureLayer.deleteFeature(self)

    def zoomToFeature(self):
        """Zoom to the Feature."""
        featureExtent = QgsRectangle(self.geometry.boundingBox())
        featureExtent.scale(1.5)  # Expand by 50%
        iface.mapCanvas().setExtent(featureExtent)
        iface.mapCanvas().refresh()

    @property
    def id(self):
        """Return the Feature's fid."""
        return self._qgsFeature.id()

    @id.setter
    def id(self, fid):
        """Set or the Feature's id."""
        self._qgsFeature.setId(fid)

    def clearId(self):
        """Set or the Feature's id."""
        self.id = -1

    @property
    def geometry(self):
        """Return the Feature's geometry."""
        return self._qgsFeature.geometry()

    @geometry.setter
    def geometry(self, g):
        """Set the Feature's geometry."""
        self._qgsFeature.setGeometry(g)

    def recalculate(self):
        """Recalculate derived data about the Feature."""
        pass

    @persistEdits
    @actionHandler(FeatureAction.trash)
    def trashFeature(self):
        """Trash a Draft Feature."""
        return deletes(self)
