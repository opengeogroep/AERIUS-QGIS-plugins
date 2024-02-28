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
        style_name = f'nl_{name}'
        print(style_name)
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

        print(classification)

        return renderer



'''
    def __create_categorized_renderer(self, style_name):
        self.plugin.log(f'generate_soilexc_renderers({style_name})')

        categorized_def = self.__categorized_defs[style_name]

        renderer = QgsCategorizedSymbolRenderer()
        renderer.setClassAttribute(categorized_def['field'])

        class_items = self.plugin.db_metadata['classes'][style_name].copy()
        class_items.append({'class_id': None, 'name': 'no data', 'color': self.__colors['nodata']})
        for class_item in class_items:
            category = QgsRendererCategory()
            category.setValue(class_item['class_id'])
            category.setLabel(class_item['name'])
            fill_color = QColor(class_item['color'])
            
            symbol = QgsFillSymbol().createSimple(self.__base_properties)
            symbol.setColor(fill_color)
            category.setSymbol(symbol)
            renderer.addCategory(category)
        return renderer
'''