# -*- coding: utf-8 -*-
from ...models.glitch import Glitch
from .field import Field
from .schema import Schema


class FieldMap(dict):

    def __init__(self, targetSchema, *args, **kwargs):
        """Create a FieldMap."""
        if not isinstance(targetSchema, Schema):
            raise Glitch(f"FieldMap targetSchema must be a Schema instance, not {type(targetSchema)}")

        self.targetSchema = targetSchema
        self.update(*args, **kwargs)

    def __setitem__(self, __key, __value) -> None:
        """Set the mapping for the given Field."""
        if not isinstance(__key, Field):
            raise Glitch(f"FieldMap keys must be QgsField objects, not {type(__key)}")

        if not self.targetSchema.hasField(__value):
            raise Glitch(f"FieldMap value {__value} not in targetSchema")

        return super().__setitem__(__key, __value)

    def __getitem__(self, __key) -> object:
        """Get the mapping for the given Field."""
        if not isinstance(__key, Field):
            raise Glitch(f"FieldMap keys must be QgsField objects, not {type(__key)}")

        return super().__getitem__(__key)

    def __repr__(self):
        """Return a string representation of the FieldMap."""
        return f"{type(self).__name__}({super().__repr__()})"

    def update(self, *args, **kwargs):
        """Update the FieldMap."""
        for k, v in dict(*args, **kwargs).items():
            self[k] = v
