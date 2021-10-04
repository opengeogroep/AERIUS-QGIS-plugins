from qgis.PyQt.QtNetwork import (
    QNetworkRequest
)

from qgis.core import (
    QgsBlockingNetworkRequest
)

from qgis.PyQt.QtCore import (
    QUrl,
    QUrlQuery
)




class AeriusOpenData():

    def __init__(self):
        self.base_url = 'https://connect.aerius.nl/opendata/base_geometries/wfs/'
        self.mime_types_dict = {'CSV': 'text/csv', 'SHAPE-ZIP': 'application/zip'}


    def __str__(self):
        return 'AeriusOpenData[]'


    def run_request(self, api_function, method, data=None, headers=None):
        if headers is None:
            headers = {'Accept': '*/*'}
        print(headers)

        url = f'{self.base_url}/{api_function}'
        print(url)

        url = QUrl(url)
        if data is not None:
            query = QUrlQuery()
            for k, v in data.items():
                query.addQueryItem(k, v)
        url.setQuery(query)

        request = QNetworkRequest(url)

        qgis_request = QgsBlockingNetworkRequest()

        err = qgis_request.get(request, True)
        print(err)

        if err > 0:
            return None

        reply = qgis_request.reply()
        return reply.content()


    def get_dataset(self, namespace, layer, output_format='SHAPE-ZIP'):
        headers = {'Accept': self.mime_types_dict[output_format]}

        api_function = ''

        data = {
            'service': 'WFS',
            'request': 'GetFeature',
            'typeName': f'{namespace}:{layer}',
            'outputFormat': output_format
        }

        #data['cql_filter'] = 'receptor_id<293081' # TODO remove! Just for testing a small data set.
        data['cql_filter'] = 'zoom_level=1'

        content = self.run_request(api_function, 'GET', data, headers)
        #print(content)
        return content
