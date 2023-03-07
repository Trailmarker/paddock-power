# -*- coding: utf-8 -*-
from os import environ, path, pathsep, getcwd

from sqlalchemy import text


def enforceForeignKeys(connection, _):
    """SQLite does not enforce foreign keys by default, but this pragma will enforce the behaviour."""
    connection.execute('pragma foreign_keys=ON')


def extendedIncludeObject(obj, name, objectType, reflected, compareTo):
    """Updated version of `include_object` from the geoalchemy2.alembic_helpers module.
    .. warning::
        This function only checks the table names, so it might exclude tables that should not be.
        In such case, you should create your own function to handle your specific table names.
    """
    if objectType == "table" and (
        name.startswith("geometry_columns")
        or name.startswith("spatial_ref_sys")
        or name.startswith("spatialite_history")
        or name.startswith("sqlite_sequence")
        or name.startswith("views_geometry_columns")
        or name.startswith("virts_geometry_columns")
        # or name.startswith("idx_")

        # Additional clauses for more recent versions of SpatiaLite
        or name.startswith("ElementaryGeometries")
        or name.startswith("SpatialIndex")
        or name.startswith("data_licenses")
    ):
        return False
    return True


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
