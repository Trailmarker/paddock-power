# -*- coding: utf-8 -*-
from os import environ, path, pathsep, getcwd

from sqlalchemy import text


def installSpatiaLiteMetadata(connection):
    """Install the SpatiaLite metadata structures for the database."""
    spatialRefSysExists = connection.execute(
        text("""select count(*) from sqlite_master where type = 'table' and name = 'spatial_ref_sys';""")).fetchone()[0]

    if spatialRefSysExists:
        print("SpatiaLite metadata already installed.")
        return

    connection.execute(text("pragma synchronous = OFF;"))
    connection.execute(text("pragma journal_mode = MEMORY;"))
    connection.execute(text("begin;"))
    connection.execute(text("select InitSpatialMetadata();"))
    connection.execute(text("commit;"))
    
    print("SpatiaLite metadata installed.")


def setSpatiaLiteLibraryPath():
    libPath = path.join(getcwd(), 'lib', 'mod_spatialite-5.0.1-win-amd64', 'mod_spatialite.dll')
    print(f"Setting SPATIALITE_LIBRARY_PATH to {libPath}")
    environ['SPATIALITE_LIBRARY_PATH'] = libPath


def loadSpatiaLite(connection, _):
    """Load the SpatiaLite extension to SQLite."""
    libPath = path.join(getcwd(), 'lib', 'mod_spatialite-5.0.1-win-amd64')
    environ['PATH'] = libPath + pathsep + environ['PATH']
    print(f"Loading SpatiaLite extension from {libPath}")
    connection.enable_load_extension(True)
    connection.execute(f"select load_extension('mod_spatialite');")

# def createEngine():
#     """Create a SQLite engine for the database and load the SpatiaLite extension."""
#     basedir = path.abspath(path.dirname(__file__))
#     connString = environ.get("DATABASE_URL") or \
#         "sqlite+pysqlite:///" + path.join(basedir, pardir, pardir, "test.sqlite")
#     engine = create_engine(connString, echo=False)
#     listen(engine, 'connect', loadSpatiaLite)

#     return engine
