# -*- coding: utf-8 -*-
from sqlalchemy import ForeignKeyConstraint

from .names import FID


def fidForeignKey(keyName, referencedFeatureModel):
    return ForeignKeyConstraint(
        [keyName],
        [f"{referencedFeatureModel.__tablename__}.{FID}"],
        use_alter=False, name=f"FK_{keyName}")
