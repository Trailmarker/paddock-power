# -*- coding: utf-8 -*-
from typing import List, Dict, Union

import sqlalchemy
from sqlalchemy import asc, desc, inspect

from . import engine


class Crud:
    def __init__(self, tableType):
        self.modelType = tableType

    def add(self,
            session: sqlalchemy.orm.session.Session,
            records: List[Dict[str, str]]
            ) -> None:
        """Add the data into database"""
        for data in records:
            newRecord = self.modelType(**data)
            session.add(newRecord)

    def query(self,
              session: sqlalchemy.orm.session.Session,
              ascending: bool = True, **kwargs: Union[int, str]
              ):
        """Get a list of data"""
        direction = asc if ascending else desc
        if kwargs:
            return session.query(self.modelType).filter_by(**kwargs).\
                order_by(direction("id")).all()
        return session.query(self.modelType).order_by(direction("id")).all()

    def update(self, instance, record: Dict[str, str]) -> None:
        """Update the data"""
        for key, value in record.items():
            setattr(instance, key, value)

    def dropTable(self) -> None:
        """Drop the table"""
        self.modelType.__table__.drop(engine)

    def truncateTable(self, session: sqlalchemy.orm.session.Session) -> None:
        """Remove all data from the table"""
        session.query(self).delete()

    def tableExists(self, tableName: str = "lake") -> bool:
        """check if the table exists"""
        inspector = inspect(engine)
        return inspector.has_table(tableName)

    def createTable(self) -> None:
        """Create all tables, will not attempt to recreate existing tables"""
        self.modelType.metadata.create_all(engine)
