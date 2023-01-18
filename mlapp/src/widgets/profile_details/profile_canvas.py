# -*- coding: utf-8 -*-
from qgis.core import QgsApplication

from ...models.glitch import Glitch
from ...spatial.elevation_profile import ElevationProfile
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import matplotlib
matplotlib.use('Qt5Agg')


class ProfileCanvas(FigureCanvasQTAgg):

    ELEVATION_BRACKET = 10.0

    def __init__(self, profile):

        if not isinstance(profile, ElevationProfile):
            raise Glitch(
                "InfrastructureProfileCanvas.__init__: profile must be a Profile")

        useMetres = (profile.maximumDistance < 1000)

        distances = profile.distances if useMetres else [
            d / 1000 for d in profile.distances]

        # maximumDistance = fencelineProfile.maximumDistance if useMetres else fencelineProfile.maximumDistance / 1000

        yMinimum = 0.0

        msShellDlg = {'fontname': 'MS Shell Dlg 2'}

        # Create a figure
        [width, height] = self._getPlotDimensionsInches()
        figure = Figure(figsize=(width, height))
        self.axes = figure.add_subplot(111)
        self.axes.plot(distances, profile.elevations)
        
        minElevation = max(0.0, profile.minimumElevation - ProfileCanvas.ELEVATION_BRACKET)
        maxElevation = profile.maximumElevation + ProfileCanvas.ELEVATION_BRACKET
        
        self.axes.set_ylim(minElevation, maxElevation)
        # self.axes.plot([0, maximumDistance], [fencelineProfile.minimumElevation, fencelineProfile.minimumElevation], 'g--', label=f"Min. : {fencelineProfile.minimumElevation}")
        # self.axes.plot([0, maximumDistance], [fencelineProfile.maximumElevation, fencelineProfile.maximumElevation], 'r--', label=f"Max. : {fencelineProfile.maximumElevation}")
        # self.axes.plot([0, maximumDistance], [fencelineProfile.meanElevation, fencelineProfile.meanElevation], 'y--', label=f"Mean : {fencelineProfile.meanElevation}")
        # self.axes.grid()
        # self.axes.legend(loc = 1)
        self.axes.set_xlabel(
            f"Distance ({'m' if useMetres else 'km'})", **msShellDlg)
        self.axes.set_ylabel("Elevation (m) (truncated)", **msShellDlg)
        self.axes.fill_between(distances,
                               profile.elevations, yMinimum, alpha=0.5)

        # figure.tight_layout()

        super().__init__(figure)


    def _getPlotDimensionsInches(self):
        # Set a reasonable initial size
        screen = QgsApplication.instance().primaryScreen()
        
        available = screen.availableGeometry()
        dpi = screen.physicalDotsPerInch()

        width = max(200, available.width() / 2)
        height = max(200, width / 3)
        
        return (width / dpi, height / dpi)

