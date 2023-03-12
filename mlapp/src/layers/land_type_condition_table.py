
import sqlite3

from qgis.PyQt.QtCore import QObject, pyqtSignal

from ..models import QtAbstractMeta, WorkspaceMixin
from ..utils import PLUGIN_NAME, qgsInfo
from .features import Edits, LandTypeCondition
from .fields import LAND_TYPE, PADDOCK, CONDITION_TYPE, ConditionType
from .interfaces import IPersistedLayer


class LandTypeConditionTable(QObject, WorkspaceMixin, IPersistedLayer, metaclass=QtAbstractMeta):

    LAYER_NAME = "Land Type Condition Table"

    editsPersisted = pyqtSignal()

    @classmethod
    def defaultName(cls):
        """Return the default name for this layer."""
        return cls.LAYER_NAME

    def __init__(self, workspaceFile, *dependentLayers):
        QObject.__init__(self)
        WorkspaceMixin.__init__(self)

        self._readOnly = False
        self._editable = False
        self.tableName = self.defaultName()

        # If not found, create
        if not self.detectInGeoPackage(workspaceFile, self.tableName):
            qgsInfo(f"{self.__class__.__name__} not found in {PLUGIN_NAME} GeoPackage. Creating new, stand by …")
            self.createInGeoPackage(workspaceFile, self.tableName)

        self.workspaceFile = workspaceFile
        self.gpkgUrl = f"{workspaceFile}|layername={self.tableName}"

    def __repr__(self):
        """Return a string representation of the Field."""
        return f"{type(self).__name__}(name={self.name()})"

    def __str__(self):
        """Convert the Field to a string representation."""
        return repr(self)

    def makeExistsQuery(self, tableName):
        return f"""
SELECT name FROM sqlite_master WHERE type='table' AND name='{tableName}'
"""

    def makeCreateQuery(self, tableName):
        return f"""
CREATE TABLE "{tableName}" (
    "{PADDOCK}" INTEGER NOT NULL,
    "{LAND_TYPE}" INTEGER NOT NULL,
    "{CONDITION_TYPE}" TEXT NOT NULL,
    CONSTRAINT "Unique" PRIMARY KEY ("{PADDOCK}", "{LAND_TYPE}")
)
"""

    def makeDropQuery(self, tableName):
        return f"""
DROP TABLE IF EXISTS "{tableName}"
"""

    def makeGetAllRecordsQuery(self, tableName):
        return f"""
SELECT * FROM "{tableName}"
"""

    def makeGetRecordQuery(self, tableName, paddockId, landTypeId):
        return f"""
SELECT * FROM "{tableName}"
WHERE "{PADDOCK}" = {paddockId} AND "{LAND_TYPE}" = {landTypeId}
"""

    def makeGetByPaddockQuery(self, tableName, paddockId):
        return f"""
SELECT * FROM "{tableName}"
WHERE "{PADDOCK}" = {paddockId}
"""

    def makeUpsertQuery(self, tableName, paddockId, landTypeId, condition):
        return f"""
INSERT INTO "{tableName}"("{PADDOCK}", "{LAND_TYPE}", "{CONDITION_TYPE}") VALUES({paddockId}, {landTypeId}, '{condition}')
ON CONFLICT("{PADDOCK}", "{LAND_TYPE}") DO UPDATE SET "{CONDITION_TYPE}"='{condition}';
"""

    def makeDeleteQuery(self, tableName, paddockId, landTypeId):
        return f"""
DELETE FROM "{tableName}" WHERE "{PADDOCK}"={paddockId} AND "{LAND_TYPE}={landTypeId};
"""

    def detectInGeoPackage(self, workspaceFile, tableName):
        """Detect a matching LandTypeConditionTable in a GeoPackage."""
        try:
            with sqlite3.connect(workspaceFile) as conn:
                cursor = conn.execute(self.makeExistsQuery(tableName=tableName))
                return cursor.fetchone() is not None
        except BaseException:
            pass
        return False

    def createInGeoPackage(self, workspaceFile, tableName):
        """Create a new LandTypeConditionTable in the GeoPackage file."""
        with sqlite3.connect(workspaceFile) as conn:
            conn.execute(self.makeCreateQuery(tableName=tableName))

    def deleteFromGeoPackage(self, workspaceFile, tableName):
        """Delete a LandTypeConditionTable from the GeoPackage file."""
        with sqlite3.connect(workspaceFile) as conn:
            conn.execute(self.makeDropQuery(tableName=tableName))

    def name(self):
        return self.defaultName()

    def id(self):
        return self.tableName

    @property
    def timeframe(self):
        """Get the current timeframe for this layer (same as that of the workspace)."""
        return self.workspace.timeframe

    def getAllRecords(self):
        with sqlite3.connect(self.workspaceFile) as conn:
            cursor = conn.execute(self.makeGetAllRecordsQuery(tableName=self.tableName))
            return cursor.fetchall()

    def getConditionRecord(self, paddockId, landTypeId):
        with sqlite3.connect(self.workspaceFile) as conn:
            cursor = conn.execute(
                self.makeGetRecordQuery(
                    tableName=self.tableName,
                    paddockId=paddockId,
                    landTypeId=landTypeId))
            return cursor.fetchone()

    def getConditionType(self, paddockId, landTypeId):
        with sqlite3.connect(self.workspaceFile) as conn:
            cursor = conn.execute(
                self.makeGetRecordQuery(
                    tableName=self.tableName,
                    paddockId=paddockId,
                    landTypeId=landTypeId))
            row = cursor.fetchone()
            if row is None:
                return ConditionType.A
            else:
                return row[3]

    def getByPaddockId(self, paddockId):
        with sqlite3.connect(self.workspaceFile) as conn:
            cursor = conn.execute(self.makeGetByPaddockQuery(tableName=self.tableName, paddockId=paddockId))
            return cursor.fetchall()

    def upsertRecord(self, paddockId, landTypeId, conditionType):
        with sqlite3.connect(self.workspaceFile) as conn:
            conn.execute(
                self.makeUpsertQuery(
                    tableName=self.tableName,
                    paddockId=paddockId,
                    landTypeId=landTypeId,
                    condition=conditionType.name))

    def upsertSplitPaddockRecord(self, splitPaddockId, crossedPaddockId):
        """Upsert the condition data for a paddock to the new paddocks into which it will be split."""

        with sqlite3.connect(self.workspaceFile) as conn:
            conn.isolation_level = None
            cursor = conn.cursor()

            cursor.execute("begin")

            try:
                # Get any existing land type records for the crossed paddock
                paddockLandTypeConditions = cursor.execute(
                    self.makeGetByPaddockQuery(
                        tableName=self.tableName,
                        paddockId=crossedPaddockId)).fetchall()

                # Upsert the land type records for the split paddock
                for paddockLandTypeCondition in paddockLandTypeConditions:
                    cursor.execute(
                        self.makeUpsertQuery(
                            tableName=self.tableName,
                            paddockId=splitPaddockId,
                            landTypeId=paddockLandTypeCondition[1],
                            condition=paddockLandTypeCondition[2]))
                cursor.execute("commit")
            except BaseException:
                cursor.execute("rollback")
                raise Exception("Error upserting split paddock condition data")

    def deleteRecord(self, paddockId, landTypeId):
        with sqlite3.connect(self.workspaceFile) as conn:
            conn.execute(
                self.makeDeleteQuery(
                    tableName=self.tableName,
                    paddockId=paddockId,
                    landTypeId=landTypeId))

    def readOnly(self):
        return self._readOnly

    def setReadOnly(self, readOnly):
        self._readOnly = readOnly

    def isEditable(self):
        return self._editable

    def startEditing(self):
        if not self._editable:
            self._editable = True
        return True

    def commitChanges(self):
        if self._editable:
            self._editable = False
        return True

    def rollBack(self):
        if self._editable:
            self._editable = False
        return True

    def copyFeature(self, feature):
        """Copy a feature using the logic (eg dependent layers) of this layer."""
        return LandTypeCondition(feature)

    def makeFeature(self):
        """Make a new, empty and default-valued feature in this layer."""
        return LandTypeCondition()

    def addFeature(self, feature):
        """Add a feature to this layer."""
        self.upsertRecord(feature.PADDOCK, feature.LAND_TYPE, feature.CONDITION_TYPE)

    def updateFeature(self, feature):
        """Update a feature in this layer."""
        self.upsertRecord(feature.PADDOCK, feature.LAND_TYPE, feature.CONDITION_TYPE)

    def deleteFeature(self, feature):
        """Delete a feature from the layer."""
        self.deleteRecord(feature.PADDOCK, feature.LAND_TYPE)

    def addFeatures(self, features):
        """Add a batch of features to this layer."""
        for feature in features:
            self.addFeature(feature)

    def recalculateFeatures(self):
        """Recalculate features in this layer."""
        return Edits()
