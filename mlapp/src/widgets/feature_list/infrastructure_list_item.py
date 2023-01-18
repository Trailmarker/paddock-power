# -*- coding: utf-8 -*-
from ...utils import PLUGIN_FOLDER
from ...widgets.profile_details.profile_details_dialog import ProfileDetailsDialog
from .feature_list_item import FeatureListItem


class InfrastructureListItem(FeatureListItem):

    def __init__(self, feature, *args, **kwargs):

        super().__init__(feature, *args, **kwargs)

        self.profileDetailsDialog = None

        self.editToolBar.addGenericAction(
            f':/plugins/{PLUGIN_FOLDER}/images/elevation.png',
            f"Show Elevation Profile",
            lambda *_: self.showProfileDetails())

    def showProfileDetails(self):
        if not self.profileDetailsDialog:
            self.profileDetailsDialog = ProfileDetailsDialog(self.feature, self)

        self.profileDetailsDialog.show()
