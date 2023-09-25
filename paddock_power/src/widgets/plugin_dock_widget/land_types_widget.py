# -*- coding: utf-8 -*-
from ...models import WorkspaceMixin
from ..feature_table import LandTypeTable, SplitFeatureTablesWidget


class LandTypesWidget(WorkspaceMixin, SplitFeatureTablesWidget):
    """A widget that shows all Pipelines associated with a Property, and allows
       new Pipelines to be sketched, planned and built, with elevation profile
       visualisation."""

    def __init__(self, parent=None):
        """Constructor."""
        WorkspaceMixin.__init__(self)
        SplitFeatureTablesWidget.__init__(self, parent)

        self.addFeatureTable("Land Types", LandTypeTable)
