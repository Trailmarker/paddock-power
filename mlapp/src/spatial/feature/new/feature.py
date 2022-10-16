# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QObject, QVariant, pyqtSlot

from qgis.core import QgsFeature, QgsField, QgsFields

from ....models.paddock_power_error import PaddockPowerError
from ..feature_status import FeatureStatus
from .feature_state_machine import FeatureStateMachine


class Feature(QObject):

    FID = "fid"
    STATUS = "Status"
    NAME = "Name"

    SCHEMA = [
        QgsField(name=FID, type=QVariant.LongLong, typeName="Integer64",
                 len=0, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name=NAME, type=QVariant.String, typeName="String",
                 len=0, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name=STATUS, type=QVariant.String, typeName="String",
                 len=0, prec=0, comment="", subType=QVariant.Invalid)
    ]

    @classmethod
    def getSchema(cls):
        return cls.SCHEMA

    @classmethod
    def checkSchema(cls, feature):
        """Check that the incoming QgsFeature's schema contains the Feature schema. Checks field names only."""
        return [field for field in cls.getSchema() if field.name() not in [f.name() for f in feature.fields()]]

    def __init__(self, feature=None):
        """Create a new Feature."""
        if isinstance(feature, QgsFeature):
            missingFields = self.checkSchema(feature)
            if missingFields:
                raise PaddockPowerError(f"Nissing fields: {missingFields}")

            self.feature = feature
        else:
            # Build an empty QgsFeature and assign it
            fields = QgsFields()
            for field in self.getSchema():
                fields.append(field)
            self.feature = QgsFeature(fields)

        self.machine = FeatureStateMachine(self)
        self.machine.start()

    def __repr__(self):
        """Return a string representation of the Feature."""
        return f"Feature({repr(self.feature)})"

    def __str__(self):
        """Convert the Feature to a string representation."""
        return repr(self)

    def id(self):
        """Return the Feature's fid."""
        return self.feature.id()

    def geometry(self):
        """Return the Feature's geometry."""
        return self.feature.geometry()

    def name(self):
        """Return the Feature's name."""
        return self.feature[Feature.NAME]

    def status(self):
        """Return the Feature's status."""
        try:
            return FeatureStatus[self.feature[Feature.STATUS]]
        except BaseException:
            return FeatureStatus.Unknown

    def setId(self, fid=-1):
        """Set or the Feature's id."""
        self.feature.setId(fid)

    def setGeometry(self, geometry):
        """Set the Feature's geometry."""
        self.feature.setGeometry(geometry)

    def setName(self, name):
        """Set the Feature's name."""
        self.feature.setAttribute(Feature.NAME, name)

    def setStatus(self, status):
        """Set the Feature's status. Should not be called directly."""
        if not isinstance(status, FeatureStatus):
            raise PaddockPowerError("status must be a FeatureStatus")
        if status == FeatureStatus.Unknown:
            raise PaddockPowerError("Feature.setStatus: trying to set FeatureStatus.Unknown")
        self.feature.setAttribute(Feature.STATUS, status.name)

    @pyqtSlot()
    def recalculate(self):
        """Recalculate derived data about the Feature."""
        pass
