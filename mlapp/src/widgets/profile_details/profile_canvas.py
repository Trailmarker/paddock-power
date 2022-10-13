# -*- coding: utf-8 -*-
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import matplotlib
matplotlib.use('Qt5Agg')

from ...layer.profile import Profile
from ...models.paddock_power_error import PaddockPowerError


class ProfileCanvas(FigureCanvasQTAgg):

    def __init__(self, profile):

        if not isinstance(profile, Profile):
            raise PaddockPowerError(
                "InfrastructureProfileCanvas.__init__: profile must be a Profile")

        useMetres = (profile.maximumDistance < 1000)

        distances = profile.distances if useMetres else [
            d / 1000 for d in profile.distances]

        # maximumDistance = fencelineProfile.maximumDistance if useMetres else fencelineProfile.maximumDistance / 1000

        yMinimum = 0.0

        msShellDlg = {'fontname': 'MS Shell Dlg 2'}

        # Create a figure
        figure = Figure()
        self.axes = figure.add_subplot(111)
        self.axes.plot(distances, profile.elevations)
        self.axes.set_ylim(0.0, profile.maximumElevation * 1.5)
        # self.axes.plot([0, maximumDistance], [fencelineProfile.minimumElevation, fencelineProfile.minimumElevation], 'g--', label=f"Min. : {fencelineProfile.minimumElevation}")
        # self.axes.plot([0, maximumDistance], [fencelineProfile.maximumElevation, fencelineProfile.maximumElevation], 'r--', label=f"Max. : {fencelineProfile.maximumElevation}")
        # self.axes.plot([0, maximumDistance], [fencelineProfile.meanElevation, fencelineProfile.meanElevation], 'y--', label=f"Mean : {fencelineProfile.meanElevation}")
        # self.axes.grid()
        # self.axes.legend(loc = 1)
        self.axes.set_xlabel(
            f"Distance ({'m' if useMetres else 'km'})", **msShellDlg)
        self.axes.set_ylabel("Elevation (m)", **msShellDlg)
        self.axes.fill_between(distances,
                               profile.elevations, yMinimum, alpha=0.5)

        figure.tight_layout()

        super(ProfileCanvas, self).__init__(figure)
