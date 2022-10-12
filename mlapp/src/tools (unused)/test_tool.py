# -*- coding: utf-8 -*-
from qgis.core import QgsApplication, QgsGeometry, QgsPoint, QgsWkbTypes
from qgis.gui import QgsIdentifyMenu, QgsMapTool, QgsMapToolIdentifyFeature
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QColor

from ..models.milestone import Milestone, PaddockPowerError
from ..utils import qgsDebug


class TestTool(QgsMapToolIdentifyFeature):
    def __init__(self, canvas, milestone):
        super(QgsMapToolIdentifyFeature, self).__init__(canvas)

        if not isinstance(milestone, Milestone):
            raise PaddockPowerError(
                "TestTool.__init__: milestone is not a Milestone.")

        self.milestone = milestone

        self.setLayer(milestone.paddockLayer)

        self.setCursor(QgsApplication.getThemeCursor(
            QgsApplication.Cursor.CrossHair))

    def canvasMoveEvent(self, event):
        """Handle the canvas move event."""
        qgsDebug("Move!")

    def canvasPressEvent(self, event):

        # super(QgsMapToolIdentifyFeature, self).canvasPressEvent(event)

        # if event.button == Qt.LeftButton:
        #     event.ignore()

        # results = QgsIdentifyMenu.findFeaturesOnCanvas(event, self.canvas, [ QgsWkbTypes.LineGeometry ])

        qgsDebug("Click!")

        # if len(results) <= 0:
        #     return


#     QgsIdentifyMenu *menu = new QgsIdentifyMenu( mCanvas );
#     menu->setAllowMultipleReturn( false );
#     menu->setExecWithSingleResult( false );

#     const QPoint globalPos = mCanvas->mapToGlobal( QPoint( e->pos().x() + 5, e->pos().y() + 5 ) );
#     const QList<QgsMapToolIdentify::IdentifyResult> selectedFeatures = menu->exec( results, globalPos );

#     menu->deleteLater();

#     if ( !selectedFeatures.empty() && selectedFeatures[0].mFeature.hasGeometry() )
#     {
#       const QgsCoordinateTransform transform = mCanvas->mapSettings().layerTransform( selectedFeatures.at( 0 ).mLayer );
#       QgsGeometry geom = selectedFeatures[0].mFeature.geometry();
#       try
#       {
#         geom.transform( transform );
#       }
#       catch ( QgsCsException & )
#       {
#         QgsDebugMsg( QStringLiteral( "Could not transform geometry from layer CRS" ) );
#       }
#       emit curveCaptured( geom );
#     }
#   }
