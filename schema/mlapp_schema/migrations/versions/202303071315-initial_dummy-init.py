"""Init

Revision ID: initial_dummy
Revises:
Create Date: 2023-03-07 13:15:00.00000

"""
# -*- coding: utf-8 -*-
from alembic import op
import sqlalchemy as sa
import geoalchemy2
import mlapp_schema.data
import mlapp_schema.data.models


# revision identifiers, used by Alembic.
revision = 'initial_dummy'
down_revision = None
branch_labels = None
depends_on = None

# create an initial dummy revision before anything else happens
# initial_dummy = op.get_bind().execute(sa.text(f"select count(*) from alembic_version;")).fetchone()[0]
# if not initial_dummy:
#     op.execute(f"insert into alembic_version (version_num) values ('initial_dummy')")

def upgrade() -> None:
    pass    

def downgrade() -> None:
    pass
