
import sqlite3

from ...utils import qgsInfo, PLUGIN_NAME
from ..schemas.condition_type import ConditionType


class ConditionTable:
    EXISTS = """
SELECT name FROM sqlite_master WHERE type='table' AND name='{tableName}'
"""

    CREATE = """
CREATE TABLE "{tableName}" (
    "Paddock" INTEGER NOT NULL,
    "Land System" INTEGER NOT NULL,
    "Condition" TEXT NOT NULL,
    CONSTRAINT "Unique" PRIMARY KEY ("Paddock", "Land System")
)
"""

    DROP = """
DROP TABLE IF EXISTS "{tableName}"
    """

    GET_RECORD = """
SELECT * FROM "{tableName}"
WHERE "Paddock" = {paddockId} AND "Land System" = {landSystemId}
    """

    GET_BY_PADDOCK = """
SELECT * FROM "{tableName}"
WHERE "Paddock" = {paddockId}
"""

    UPSERT = """
INSERT INTO "{tableName}"("Paddock", "Land System", "Condition") VALUES({paddockId}, {landSystemId}, '{conditionType}')
ON CONFLICT("Paddock", "Land System") DO UPDATE SET "Condition"='{conditionType}';
"""

    DELETE = """
DELETE FROM "{tableName}" WHERE "Paddock"={paddockId} AND "Land System"={landSystemId};
"""

    def detectInGeoPackage(self, gpkgFile, tableName):
        """Detect a matching ConditionTable in a GeoPackage."""
        try:
            with sqlite3.connect(gpkgFile) as conn:
                cursor = conn.execute(ConditionTable.EXISTS.format(tableName=tableName))
                return cursor.fetchone() is not None
        except BaseException:
            pass
        return False

    def createInGeoPackage(self, gpkgFile, tableName):
        """Create a new ConditionTable in the GeoPackage file."""
        with sqlite3.connect(gpkgFile) as conn:
            conn.execute(self.CREATE.format(tableName=tableName))

    def deleteFromGeoPackage(self, gpkgFile, tableName):
        """Delete a ConditionTable from the GeoPackage file."""
        with sqlite3.connect(gpkgFile) as conn:
            conn.execute(self.DROP.format(tableName=tableName))

    def __init__(self, gpkgFile, tableName):
        # If not found, create
        if not self.detectInGeoPackage(gpkgFile, tableName):
            qgsInfo(f"{self.__class__.__name__} not found in {PLUGIN_NAME} GeoPackage. Creating new, stand by …")
            self.createInGeoPackage(gpkgFile, tableName)

        self.gpkgFile = gpkgFile
        self.tableName = tableName
        self._gpkgUrl = f"{gpkgFile}|layername={tableName}"

    def name(self):
        return self.tableName

    def getRecord(self, paddockId, landSystemId):
        with sqlite3.connect(self.gpkgFile) as conn:
            cursor = conn.execute(
                self.GET_RECORD.format(
                    tableName=self.tableName,
                    paddockId=paddockId,
                    landSystemId=landSystemId))
            return cursor.fetchone()

    def getCondition(self, paddockId, landSystemId):
        with sqlite3.connect(self.gpkgFile) as conn:
            cursor = conn.execute(
                self.GET_RECORD.format(
                    tableName=self.tableName,
                    paddockId=paddockId,
                    landSystemId=landSystemId))
            row = cursor.fetchone()
            if row is None:
                return ConditionType.A
            else:
                return row[3]

    def getByPaddockId(self, paddockId):
        with sqlite3.connect(self.gpkgFile) as conn:
            cursor = conn.execute(self.GET_BY_PADDOCK.format(tableName=self.tableName, paddockId=paddockId))
            return cursor.fetchall()

    def upsert(self, paddockId, landSystemId, conditionType):
        with sqlite3.connect(self.gpkgFile) as conn:
            conn.execute(
                self.UPSERT.format(
                    tableName=self.tableName,
                    paddockId=paddockId,
                    landSystemId=landSystemId,
                    conditionType=conditionType.name))

    def delete(self, paddockId, landSystemId):
        with sqlite3.connect(self.gpkgFile) as conn:
            conn.execute(
                self.DELETE.format(
                    tableName=self.tableName,
                    paddockId=paddockId,
                    landSystemId=landSystemId))
