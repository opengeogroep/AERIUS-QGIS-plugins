import os

from qgis.PyQt.QtGui import QIcon
from qgis.core import QgsProcessingProvider

from .relate_difference import RelateDifferenceAlgorithm
from .relate_sum import RelateSumAlgorithm


class ImaerProvider(QgsProcessingProvider):

    def loadAlgorithms(self, *args, **kwargs):
        self.addAlgorithm(RelateDifferenceAlgorithm())
        self.addAlgorithm(RelateSumAlgorithm())

    def id(self, *args, **kwargs):
        """The ID of your plugin, used for identifying the provider.
        This string should be a unique, short, character only string,
        eg "qgis" or "gdal". This string should not be localised.
        """
        return 'imaer'

    def name(self, *args, **kwargs):
        """The human friendly name of your plugin in Processing.
        This string should be as short as possible (e.g. "Lastools", not
        "Lastools version 1.0.1 64-bit") and localised.
        """
        return self.tr('IMAER tools')

    def icon(self):
        """Should return a QIcon which is used for your provider inside
        the Processing toolbox.
        """
        plugin_dir = os.path.dirname(os.path.dirname(__file__))
        icon_fn = os.path.join(plugin_dir, 'img', 'icon_import_calc_result.svg')
        icon = QIcon(icon_fn)
        return icon
