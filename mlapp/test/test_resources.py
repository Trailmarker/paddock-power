# coding=utf-8
import unittest

from qgis.PyQt.QtGui import QIcon


class DialogTest(unittest.TestCase):
    """Test rerources work."""

    def setUp(self):
        """Runs before each test."""
        pass

    def tearDown(self):
        """Runs after each test."""
        pass

    def test_icon_png(self):
        """Test we can click OK."""
        path = ':/plugins/PaddockPower/icon.png'
        icon = QIcon(path)
        self.assertFalse(icon.isNull())


if __name__ == "__main__":
    suite = unittest.makeSuite(PaddockPowerResourcesTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
