"""Add all MLA Paddock Power tables

Revision ID: 74fa66ce6dde
Revises: 7abf0c8f8043
Create Date: 2023-03-07 22:08:06.633456

"""
# -*- coding: utf-8 -*-
from alembic import op
import sqlalchemy as sa
import geoalchemy2
import mlapp_schema.data
import mlapp_schema.data.models 

from geoalchemy2 import Geometry

# revision identifiers, used by Alembic.
revision = '74fa66ce6dde'
down_revision = '7abf0c8f8043'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_geospatial_table('Base Paddocks',
    sa.Column('Build Fence', sa.Integer(), nullable=True),
    sa.Column('fid', sa.Integer(), nullable=False),
    sa.Column('geometry', Geometry(geometry_type='MULTIPOLYGON', srid=7845, spatial_index=False, from_text='ST_GeomFromEWKT', name='geometry'), nullable=False),
    sa.Column('Area (km²)', sa.Float(), nullable=False),
    sa.Column('Perimeter (km)', sa.Float(), nullable=False),
    sa.Column('Name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('fid')
    )
    op.create_geospatial_index('idx_Base Paddocks_geometry', 'Base Paddocks', ['geometry'], unique=False, postgresql_using='gist', postgresql_ops={})
    op.create_geospatial_table('Boundary',
    sa.Column('fid', sa.Integer(), nullable=False),
    sa.Column('geometry', Geometry(geometry_type='MULTIPOLYGON', srid=7845, spatial_index=False, from_text='ST_GeomFromEWKT', name='geometry'), nullable=False),
    sa.Column('Area (km²)', sa.Float(), nullable=False),
    sa.Column('Perimeter (km)', sa.Float(), nullable=False),
    sa.Column('Timeframe', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('fid')
    )
    op.create_geospatial_index('idx_Boundary_geometry', 'Boundary', ['geometry'], unique=False, postgresql_using='gist', postgresql_ops={})
    op.create_geospatial_table('Fences',
    sa.Column('Build Order', sa.Integer(), nullable=False),
    sa.Column('fid', sa.Integer(), nullable=False),
    sa.Column('geometry', Geometry(geometry_type='LINESTRING', srid=7845, spatial_index=False, from_text='ST_GeomFromEWKT', name='geometry'), nullable=False),
    sa.Column('Length (km)', sa.Float(), nullable=False),
    sa.Column('Name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('fid')
    )
    op.create_geospatial_index('idx_Fences_geometry', 'Fences', ['geometry'], unique=False, postgresql_using='gist', postgresql_ops={})
    op.create_geospatial_table('Land Types',
    sa.Column('Land Type Name', sa.String(), nullable=False),
    sa.Column("Best AE/km² (if Condition is 'A')", sa.Float(), nullable=False),
    sa.Column('fid', sa.Integer(), nullable=False),
    sa.Column('geometry', Geometry(geometry_type='MULTIPOLYGON', srid=7845, spatial_index=False, from_text='ST_GeomFromEWKT', name='geometry'), nullable=False),
    sa.Column('Area (km²)', sa.Float(), nullable=False),
    sa.Column('Perimeter (km)', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('fid')
    )
    op.create_geospatial_index('idx_Land Types_geometry', 'Land Types', ['geometry'], unique=False, postgresql_using='gist', postgresql_ops={})
    op.create_geospatial_table('Paddock Land Types',
    sa.Column('Paddock', sa.Integer(), nullable=False),
    sa.Column('Land Type', sa.Integer(), nullable=False),
    sa.Column('Paddock Name', sa.String(), nullable=False),
    sa.Column('Land Type Name', sa.String(), nullable=False),
    sa.Column('Condition', sa.String(), nullable=False),
    sa.Column('fid', sa.Integer(), nullable=False),
    sa.Column('Watered Area (km²)', sa.Float(), nullable=False),
    sa.Column('AE/km²', sa.Float(), nullable=False),
    sa.Column('Potential AE/km²', sa.Float(), nullable=False),
    sa.Column('AE', sa.Float(), nullable=False),
    sa.Column('Potential AE', sa.Float(), nullable=False),
    sa.Column('geometry', Geometry(geometry_type='MULTIPOLYGON', srid=7845, spatial_index=False, from_text='ST_GeomFromEWKT', name='geometry'), nullable=False),
    sa.Column('Area (km²)', sa.Float(), nullable=False),
    sa.Column('Perimeter (km)', sa.Float(), nullable=False),
    sa.Column('Timeframe', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('fid')
    )
    op.create_geospatial_index('idx_Paddock Land Types_geometry', 'Paddock Land Types', ['geometry'], unique=False, postgresql_using='gist', postgresql_ops={})
    op.create_geospatial_table('Paddocks',
    sa.Column('Paddock', sa.Integer(), nullable=False),
    sa.Column('Build Fence', sa.Integer(), nullable=True),
    sa.Column('fid', sa.Integer(), nullable=False),
    sa.Column('Watered Area (km²)', sa.Float(), nullable=False),
    sa.Column('AE/km²', sa.Float(), nullable=False),
    sa.Column('Potential AE/km²', sa.Float(), nullable=False),
    sa.Column('AE', sa.Float(), nullable=False),
    sa.Column('Potential AE', sa.Float(), nullable=False),
    sa.Column('geometry', Geometry(geometry_type='MULTIPOLYGON', srid=7845, spatial_index=False, from_text='ST_GeomFromEWKT', name='geometry'), nullable=False),
    sa.Column('Area (km²)', sa.Float(), nullable=False),
    sa.Column('Perimeter (km)', sa.Float(), nullable=False),
    sa.Column('Timeframe', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('fid')
    )
    op.create_geospatial_index('idx_Paddocks_geometry', 'Paddocks', ['geometry'], unique=False, postgresql_using='gist', postgresql_ops={})
    op.create_geospatial_table('Pipelines',
    sa.Column('fid', sa.Integer(), nullable=False),
    sa.Column('geometry', Geometry(geometry_type='LINESTRING', srid=7845, spatial_index=False, from_text='ST_GeomFromEWKT', name='geometry'), nullable=False),
    sa.Column('Length (km)', sa.Float(), nullable=False),
    sa.Column('Name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('fid')
    )
    op.create_geospatial_index('idx_Pipelines_geometry', 'Pipelines', ['geometry'], unique=False, postgresql_using='gist', postgresql_ops={})
    op.create_geospatial_table('Watered Areas',
    sa.Column('Paddock', sa.Integer(), nullable=False),
    sa.Column('Watered', sa.String(), nullable=False),
    sa.Column('fid', sa.Integer(), nullable=False),
    sa.Column('geometry', Geometry(geometry_type='MULTIPOLYGON', srid=7845, spatial_index=False, from_text='ST_GeomFromEWKT', name='geometry'), nullable=False),
    sa.Column('Area (km²)', sa.Float(), nullable=False),
    sa.Column('Perimeter (km)', sa.Float(), nullable=False),
    sa.Column('Timeframe', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('fid')
    )
    op.create_geospatial_index('idx_Watered Areas_geometry', 'Watered Areas', ['geometry'], unique=False, postgresql_using='gist', postgresql_ops={})
    op.create_geospatial_table('Waterpoint Buffers',
    sa.Column('Waterpoint', sa.Integer(), nullable=False),
    sa.Column('Paddock', sa.Integer(), nullable=False),
    sa.Column('Grazing Radius Type', sa.String(), nullable=False),
    sa.Column('Grazing Radius (m)', sa.Float(), nullable=False),
    sa.Column('fid', sa.Integer(), nullable=False),
    sa.Column('geometry', Geometry(geometry_type='MULTIPOLYGON', srid=7845, spatial_index=False, from_text='ST_GeomFromEWKT', name='geometry'), nullable=False),
    sa.Column('Area (km²)', sa.Float(), nullable=False),
    sa.Column('Perimeter (km)', sa.Float(), nullable=False),
    sa.Column('Status', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('fid')
    )
    op.create_geospatial_index('idx_Waterpoint Buffers_geometry', 'Waterpoint Buffers', ['geometry'], unique=False, postgresql_using='gist', postgresql_ops={})
    op.drop_table('ElementaryGeometries')
    op.drop_table('data_licenses')
    op.drop_table('SpatialIndex')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('SpatialIndex',
    sa.Column('f_table_name', sa.TEXT(), nullable=True),
    sa.Column('f_geometry_column', sa.TEXT(), nullable=True),
    sa.Column('search_frame', sa.BLOB(), nullable=True)
    )
    op.create_table('data_licenses',
    sa.Column('id', sa.INTEGER(), nullable=True),
    sa.Column('name', sa.TEXT(), nullable=False),
    sa.Column('url', sa.TEXT(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('ElementaryGeometries',
    sa.Column('db_prefix', sa.TEXT(), nullable=True),
    sa.Column('f_table_name', sa.TEXT(), nullable=True),
    sa.Column('f_geometry_column', sa.TEXT(), nullable=True),
    sa.Column('origin_rowid', sa.INTEGER(), nullable=True),
    sa.Column('item_no', sa.INTEGER(), nullable=True),
    sa.Column('geometry', sa.BLOB(), nullable=True)
    )
    op.drop_geospatial_index('idx_Waterpoint Buffers_geometry', table_name='Waterpoint Buffers', postgresql_using='gist', column_name='geometry')
    op.drop_geospatial_table('Waterpoint Buffers')
    op.drop_geospatial_index('idx_Watered Areas_geometry', table_name='Watered Areas', postgresql_using='gist', column_name='geometry')
    op.drop_geospatial_table('Watered Areas')
    op.drop_geospatial_index('idx_Pipelines_geometry', table_name='Pipelines', postgresql_using='gist', column_name='geometry')
    op.drop_geospatial_table('Pipelines')
    op.drop_geospatial_index('idx_Paddocks_geometry', table_name='Paddocks', postgresql_using='gist', column_name='geometry')
    op.drop_geospatial_table('Paddocks')
    op.drop_geospatial_index('idx_Paddock Land Types_geometry', table_name='Paddock Land Types', postgresql_using='gist', column_name='geometry')
    op.drop_geospatial_table('Paddock Land Types')
    op.drop_geospatial_index('idx_Land Types_geometry', table_name='Land Types', postgresql_using='gist', column_name='geometry')
    op.drop_geospatial_table('Land Types')
    op.drop_geospatial_index('idx_Fences_geometry', table_name='Fences', postgresql_using='gist', column_name='geometry')
    op.drop_geospatial_table('Fences')
    op.drop_geospatial_index('idx_Boundary_geometry', table_name='Boundary', postgresql_using='gist', column_name='geometry')
    op.drop_geospatial_table('Boundary')
    op.drop_geospatial_index('idx_Base Paddocks_geometry', table_name='Base Paddocks', postgresql_using='gist', column_name='geometry')
    op.drop_geospatial_table('Base Paddocks')
    # ### end Alembic commands ###
