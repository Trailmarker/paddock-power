# -*- coding: utf-8 -*-
from os import environ, path, pathsep, getcwd

from sqlalchemy import create_engine, text
from sqlalchemy.event import listen


def loadSpatiaLite(conn, _):
    libPath = path.join(getcwd(), 'lib', 'mod_spatialite-5.0.1-win-amd64')
    environ['PATH'] = libPath + pathsep + environ['PATH']
    conn.enable_load_extension(True)
    conn.execute(f"select load_extension('mod_spatialite')")


def test_createEngine():
    """Test create_engine()"""
    engine = create_engine('sqlite+pysqlite:///:memory:', echo=True)
    assert engine is not None


def test_createEngineAndLoadSpatiaLite():
    engine = create_engine('sqlite+pysqlite:///:memory:', echo=True)
    assert engine is not None
    listen(engine, 'connect', loadSpatiaLite)


def test_createEngineAndCreateTable():
    """Test creating an engine and a table"""
    engine = create_engine('sqlite+pysqlite:///test.sqlite', echo=True)
    listen(engine, 'connect', loadSpatiaLite)

    with engine.connect() as conn:
        conn.execute(text('create table if not exists Test (Id INTEGER PRIMARY KEY, Name TEXT)'))
        result = conn.execute(text('select * from Test'))
        assert result is not None