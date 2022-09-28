# -*- coding: utf-8 -*-
from .fenceline_profile import FencelineProfile
from ...models.paddock_power_error import PaddockPowerError

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import matplotlib
matplotlib.use('Qt5Agg')


class FencelineProfileCanvas(FigureCanvasQTAgg):

    def __init__(self, fencelineProfile):

        if not isinstance(fencelineProfile, FencelineProfile):
            raise PaddockPowerError(
                "FencelineProfileCanvas.__init__: fencelineProfile is not a FencelineProfile.")

        useMetres = (fencelineProfile.maximumDistance < 1000)

        distances = fencelineProfile.distances if useMetres else [
            d / 1000 for d in fencelineProfile.distances]
        maximumDistance = fencelineProfile.maximumDistance if useMetres else fencelineProfile.maximumDistance / 1000

        yMinimum = 0.0

        msShellDlg = {'fontname': 'MS Shell Dlg 2'}

        # Create a figure
        figure = Figure(figsize=(10, 4))
        self.axes = figure.add_subplot(111)
        self.axes.plot(distances, fencelineProfile.elevations)
        self.axes.set_ylim(0.0, fencelineProfile.maximumElevation * 1.5)
        # self.axes.plot([0, maximumDistance], [fencelineProfile.minimumElevation, fencelineProfile.minimumElevation], 'g--', label=f"Min. : {fencelineProfile.minimumElevation}")
        # self.axes.plot([0, maximumDistance], [fencelineProfile.maximumElevation, fencelineProfile.maximumElevation], 'r--', label=f"Max. : {fencelineProfile.maximumElevation}")
        # self.axes.plot([0, maximumDistance], [fencelineProfile.meanElevation, fencelineProfile.meanElevation], 'y--', label=f"Mean : {fencelineProfile.meanElevation}")
        # self.axes.grid()
        # self.axes.legend(loc = 1)
        self.axes.set_xlabel(
            f"Distance ({'m' if useMetres else 'km'})", **msShellDlg)
        self.axes.set_ylabel("Elevation (m)", **msShellDlg)
        self.axes.fill_between(fencelineProfile.distances,
                               fencelineProfile.elevations, yMinimum, alpha=0.5)

        figure.tight_layout()

        super(FencelineProfileCanvas, self).__init__(figure)
