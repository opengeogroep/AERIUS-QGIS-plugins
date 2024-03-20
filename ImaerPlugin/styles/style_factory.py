from qgis.PyQt.QtGui import (
    QColor,
    QFont
)

from qgis.core import (
    QgsGraduatedSymbolRenderer,
    QgsRendererRange,
    QgsClassificationRange,
    QgsFillSymbol,
    QgsMarkerSymbol,
    QgsPalLayerSettings,
    QgsVectorLayerSimpleLabeling,
    QgsTextFormat
)

from .classifications import classifications

class StyleFactory():

    def __init__(self, plugin):
        self.plugin = plugin

    __base_properties = {
        'color': "135,135,135,255", 'joinstyle': 'bevel','style': 'solid',
        'outline_color': '35,35,35,255', 'outline_style': 'solid', 'outline_width': '0.05', 'outline_width_unit': 'MM'
    }

    def __init__(self, plugin):
        self.plugin = plugin
    
    def create_renderer(self, name, geometry_type):
        country_setting = self.plugin.settings.value('imaer_plugin/country', defaultValue='')
        if country_setting == '':
            return None

        style_name = f'{country_setting.lower()}_{name}'
        classification = classifications[style_name]
        
        result = None
        if geometry_type == 'point':
            if classification['render_type'] == 'graduated':
                result = self.__create_graduated_point_renderer(classification)
        elif geometry_type == 'polygon':
            if classification['render_type'] == 'graduated':
                result = self.__create_graduated_polygon_renderer(classification)

        return result

    def __create_graduated_point_renderer(self, classification):
        renderer = QgsGraduatedSymbolRenderer()

        for cls in classification['classes']:
            symbol = QgsMarkerSymbol()

            # Fill color
            fill_color = QColor(f'#{cls[3]}')
            fill_color.setAlphaF(0.66)
            symbol.setColor(fill_color)

            # Stroke color
            outline_color = QColor(f'#{cls[3]}')
            symbol_0 = symbol.symbolLayers()[0]
            symbol_0.setStrokeColor(outline_color)

            # Size
            symbol_0.setSize(2)

            renderer.addClassRange(QgsRendererRange(QgsClassificationRange(cls[0], cls[1], cls[2]), symbol))

        return renderer

    def __create_graduated_polygon_renderer(self, classification):
        renderer = QgsGraduatedSymbolRenderer()

        for cls in classification['classes']:
            symbol = QgsFillSymbol().createSimple(self.__base_properties)

            # Fill color
            fill_color = QColor(f'#{cls[3]}')
            fill_color.setAlphaF(0.66)
            symbol.setColor(fill_color)

            # Stroke color
            outline_color = QColor(f'#{cls[3]}')
            symbol_0 = symbol.symbolLayers()[0]
            symbol_0.setStrokeColor(outline_color)

            renderer.addClassRange(QgsRendererRange(QgsClassificationRange(cls[0], cls[1], cls[2]), symbol))

        return renderer

    def create_labeling(self, field_name, minimum_scale=8000):
        layer_settings = QgsPalLayerSettings()

        text_format = QgsTextFormat()
        text_format.setFont(QFont("Sans"))
        text_format.setSize(8)

        text_color = QColor('#000000')
        text_format.setOpacity(0.5)
        text_format.setColor(text_color)

        layer_settings.setFormat(text_format)

        layer_settings.fieldName = field_name

        layer_settings.minimumScale = minimum_scale
        layer_settings.scaleVisibility = True

        layer_settings.decimals = 3
        layer_settings.formatNumbers = True

        layer_settings.enabled = True

        result = QgsVectorLayerSimpleLabeling(layer_settings)
        return result
