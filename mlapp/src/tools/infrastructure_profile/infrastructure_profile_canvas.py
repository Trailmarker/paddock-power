# -*- coding: utf-8 -*-
from .infrastructure_profile import InfrastructureProfile
from ...models.paddock_power_error import PaddockPowerError
from ...utils import qgsDebug

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import matplotlib
matplotlib.use('Qt5Agg')


class InfrastructureProfileCanvas(FigureCanvasQTAgg):

    def __init__(self, fencelineProfile):

        if not isinstance(fencelineProfile, InfrastructureProfile):
            raise PaddockPowerError(
                "InfrastructureProfileCanvas.__init__: fencelineProfile is not a InfrastructureProfile.")

        useMetres = (fencelineProfile.maximumDistance < 1000)

        qgsDebug(f"InfrastructureProfileCanvas.__init__: useMetres={useMetres}")

        distances = fencelineProfile.distances if useMetres else [
            d / 1000 for d in fencelineProfile.distances]

        qgsDebug(f"InfrastructureProfileCanvas.__init__: distances={str(distances)}")

        # maximumDistance = fencelineProfile.maximumDistance if useMetres else fencelineProfile.maximumDistance / 1000

        yMinimum = 0.0

        msShellDlg = {'fontname': 'MS Shell Dlg 2'}

        # Create a figure
        figure = Figure(figsize=(20, 6))
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
        self.axes.fill_between(distances,
                               fencelineProfile.elevations, yMinimum, alpha=0.5)

        figure.tight_layout()

        super(InfrastructureProfileCanvas, self).__init__(figure)


