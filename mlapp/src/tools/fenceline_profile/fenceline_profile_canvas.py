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

        # Extract fenceline profile axes
        distances = [distance for (distance, _) in self.fenceLineProfile.profileData]
        elevations = [elevation for (_, elevation)
              in self.fenceLineProfile.profileData]

        minimumZ = round(min(elevations), 1)
        maximumZ = round(max(elevations), 1)
        meanZ = round(sum(elevations) / len(elevations), 1)

        maximumDistance = distances[-1]

        # Create a figure
        figure = Figure(figsize = (10, 4))
        self.axes = figure.add_subplot(111)
        self.axes.plot(distances, elevations)
        self.axes.plot([0, maximumDistance], [minimumZ, minimumZ], 'g--', label=f"Min. : {minimumZ}")
        self.axes.plot([0, maximumDistance], [maximumZ, maximumZ], 'r--', label=f"Max. : {maximumZ}")
        self.axes.plot([0, maximumDistance], [meanZ, meanZ], 'y--', label=f"Mean : {meanZ}")
        self.axes.grid()
        self.axes.legend(loc = 1)
        self.axes.set_xlabel("Distance (m)")
        self.axes.set_ylabel("Elevation (m)")
        self.axes.fill_between(distances, elevations, minimumZ, alpha=0.5)

        super(FencelineProfileCanvas, self).__init__(figure)
