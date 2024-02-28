from qgis.PyQt.QtGui import (
    QColor,
    #QFont
)

from qgis.core import (
    QgsGraduatedSymbolRenderer,
    QgsRendererRange,
    QgsClassificationRange,
    QgsFillSymbol,
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
    
    def create_renderer(self, name):
        country_setting = self.plugin.settings.value('imaer_plugin/country', defaultValue='')
        if country_setting == '':
            return None

        style_name = f'{country_setting.lower()}_{name}'
        classification = classifications[style_name]
        
        result = None
        if classification['render_type'] == 'graduated':
            result = self.__create_graduated_renderer(classification)

        return result

    def __create_graduated_renderer(self, classification):
        renderer = QgsGraduatedSymbolRenderer()
        renderer.setClassAttribute(classification['field'])

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
