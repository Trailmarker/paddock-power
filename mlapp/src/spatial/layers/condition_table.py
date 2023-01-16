
import sqlite3

from qgis.PyQt.QtCore import QObject, pyqtSignal

from ...utils import qgsInfo, PLUGIN_NAME
from ..fields.condition_type import ConditionType
from ..fields.names import LAND_TYPE, PADDOCK, CONDITION_TYPE


class ConditionTable(QObject):
    featuresPersisted = pyqtSignal(list)

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

    def makeUpsertQuery(self, tableName, paddockId, landTypeId, conditionType):
        return f"""
INSERT INTO "{tableName}"("{PADDOCK}", "{LAND_TYPE}", "{CONDITION_TYPE}") VALUES({paddockId}, {landTypeId}, '{conditionType}')
ON CONFLICT("{PADDOCK}", "{LAND_TYPE}") DO UPDATE SET "{CONDITION_TYPE}"='{conditionType}';
"""

    def makeDeleteQuery(self, tableName, paddockId, landTypeId):
        return f"""
DELETE FROM "{tableName}" WHERE "{PADDOCK}"={paddockId} AND "{LAND_TYPE}={landTypeId};
"""

    def detectInGeoPackage(self, gpkgFile, tableName):
        """Detect a matching ConditionTable in a GeoPackage."""
        try:
            with sqlite3.connect(gpkgFile) as conn:
                cursor = conn.execute(self.makeExistsQuery(tableName=tableName))
                return cursor.fetchone() is not None
        except BaseException:
            pass
        return False

    def createInGeoPackage(self, gpkgFile, tableName):
        """Create a new ConditionTable in the GeoPackage file."""
        with sqlite3.connect(gpkgFile) as conn:
            conn.execute(self.makeCreateQuery(tableName=tableName))

    def deleteFromGeoPackage(self, gpkgFile, tableName):
        """Delete a ConditionTable from the GeoPackage file."""
        with sqlite3.connect(gpkgFile) as conn:
            conn.execute(self.makeDropQuery(tableName=tableName))

    def __init__(self, project, gpkgFile, tableName):
        super().__init__()

        # Stash the Paddock Power project
        assert(project is not None)
        self._project = project

        # If not found, create
        if not self.detectInGeoPackage(gpkgFile, tableName):
            qgsInfo(f"{self.__class__.__name__} not found in {PLUGIN_NAME} GeoPackage. Creating new, stand by …")
            self.createInGeoPackage(gpkgFile, tableName)

        self.gpkgFile = gpkgFile
        self.tableName = tableName
        self._gpkgUrl = f"{gpkgFile}|layername={tableName}"

    def name(self):
        return self.tableName

    def getRecord(self, paddockId, landTypeId):
        with sqlite3.connect(self.gpkgFile) as conn:
            cursor = conn.execute(
                self.makeGetRecordQuery(
                    tableName=self.tableName,
                    paddockId=paddockId,
                    landTypeId=landTypeId))
            return cursor.fetchone()

    def getCondition(self, paddockId, landTypeId):
        with sqlite3.connect(self.gpkgFile) as conn:
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
        with sqlite3.connect(self.gpkgFile) as conn:
            cursor = conn.execute(self.makeGetByPaddockQuery(tableName=self.tableName, paddockId=paddockId))
            return cursor.fetchall()

    def upsert(self, paddockId, landTypeId, conditionType):
        with sqlite3.connect(self.gpkgFile) as conn:
            conn.execute(
                self.makeUpsertQuery(
                    tableName=self.tableName,
                    paddockId=paddockId,
                    landTypeId=landTypeId,
                    conditionType=conditionType.name))
        self.featuresPersisted.emit([paddockId])

    def delete(self, paddockId, landTypeId):
        with sqlite3.connect(self.gpkgFile) as conn:
            conn.execute(
                self.makeDeleteQuery(
                    tableName=self.tableName,
                    paddockId=paddockId,
                    landTypeId=landTypeId))
        self.featuresPersisted.emit([paddockId])
