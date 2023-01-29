
import sqlite3

from qgis.PyQt.QtCore import pyqtSignal

from ...utils import qgsInfo, PLUGIN_NAME
from ..fields.condition_type import ConditionType
from ..fields.names import LAND_TYPE, PADDOCK, CONDITION_TYPE
from ..fields.timeframe import Timeframe
from ..layers.mixins.workspace_connection_mixin import WorkspaceConnectionMixin


class ConditionTable(WorkspaceConnectionMixin):

    NAME = "ConditionTable"

    featuresChanged = pyqtSignal(list)

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
        """Detect a matching ConditionTable in a GeoPackage."""
        try:
            with sqlite3.connect(workspaceFile) as conn:
                cursor = conn.execute(self.makeExistsQuery(tableName=tableName))
                return cursor.fetchone() is not None
        except BaseException:
            pass
        return False

    def createInGeoPackage(self, workspaceFile, tableName):
        """Create a new ConditionTable in the GeoPackage file."""
        with sqlite3.connect(workspaceFile) as conn:
            conn.execute(self.makeCreateQuery(tableName=tableName))

    def deleteFromGeoPackage(self, workspaceFile, tableName):
        """Delete a ConditionTable from the GeoPackage file."""
        with sqlite3.connect(workspaceFile) as conn:
            conn.execute(self.makeDropQuery(tableName=tableName))

    def __init__(self, workspaceFile):
        super().__init__()

        self.tableName = ConditionTable.NAME

        # If not found, create
        if not self.detectInGeoPackage(workspaceFile, self.tableName):
            qgsInfo(f"{self.__class__.__name__} not found in {PLUGIN_NAME} GeoPackage. Creating new, stand by …")
            self.createInGeoPackage(workspaceFile, self.tableName)

        self.workspaceFile = workspaceFile
        self.gpkgUrl = f"{workspaceFile}|layername={self.tableName}"

    def name(self):
        return self.tableName

    def id(self):
        return self.tableName

    # Workspace interface
    @property
    def connectedToWorkspace(self):
        """Are we both connected to the workspace and not temporarily blocked."""
        return self._workspace is not None

    @property
    def workspace(self):
        f"""The {PLUGIN_NAME} workspace we are connected to."""
        return self._workspace

    @property
    def currentTimeframe(self):
        """Get the current timeframe for this layer (same as that of the workspace)."""
        return self.workspace.currentTimeframe if self.connectedToWorkspace else Timeframe.Undefined

    def connectWorkspace(self, workspace):
        """Hook it up to uor veins."""
        self._workspace = workspace

    def getAllRecords(self):
        with sqlite3.connect(self.workspaceFile) as conn:
            cursor = conn.execute(self.makeGetAllRecordsQuery(tableName=self.tableName))
            return cursor.fetchall()

    def getRecord(self, paddockId, landTypeId):
        with sqlite3.connect(self.workspaceFile) as conn:
            cursor = conn.execute(
                self.makeGetRecordQuery(
                    tableName=self.tableName,
                    paddockId=paddockId,
                    landTypeId=landTypeId))
            return cursor.fetchone()

    def getCondition(self, paddockId, landTypeId):
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

    def upsert(self, paddockId, landTypeId, conditionType):
        with sqlite3.connect(self.workspaceFile) as conn:
            conn.execute(
                self.makeUpsertQuery(
                    tableName=self.tableName,
                    paddockId=paddockId,
                    landTypeId=landTypeId,
                    condition=conditionType.name))
        self.workspace.featuresChanged.emit([self])

    def upsertSplit(self, splitPaddockId, crossedPaddockId):
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

    def delete(self, paddockId, landTypeId):
        with sqlite3.connect(self.workspaceFile) as conn:
            conn.execute(
                self.makeDeleteQuery(
                    tableName=self.tableName,
                    paddockId=paddockId,
                    landTypeId=landTypeId))
        # self.featuresChanged.emit([self])
