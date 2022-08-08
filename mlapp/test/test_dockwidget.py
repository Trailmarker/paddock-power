# coding=utf-8
import unittest

from qgis.PyQt.QtGui import QDockWidget

from dockwidget import DockWidget

from utilities import get_qgis_app

QGIS_APP = get_qgis_app()


class DockWidgetTest(unittest.TestCase):
    """Test dockwidget works."""

    def setUp(self):
        """Runs before each test."""
        self.dockwidget = DockWidget(None)

    def tearDown(self):
        """Runs after each test."""
        self.dockwidget = None

    def test_dockwidget_ok(self):
        """Test we can click OK."""
        pass

if __name__ == "__main__":
    suite = unittest.makeSuite(DockWidgetTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

