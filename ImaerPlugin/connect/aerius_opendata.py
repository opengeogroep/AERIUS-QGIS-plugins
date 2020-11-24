import urllib.parse

from .network import NetworkAccessManager, RequestsException




class AeriusOpenData():

    def __init__(self):
        self.base_url = 'https://connect.aerius.nl/opendata/wfs'
        self.mime_types_dict = {'CSV': 'text/csv', 'SHAPE-ZIP': 'application/zip'}


    def __str__(self):
        return 'AeriusOpenData[]'


    def run_request(self, api_function, method, data=None, headers=None):

        if headers is None:
            headers = {'Accept': '*/*'}
        print(headers)

        url = f'{self.base_url}/{api_function}'
        print(url)

        nam = NetworkAccessManager()
        nam.debug = True

        if method == 'GET':
            if data is not None:
                #print(data)
                params = urllib.parse.urlencode(data)
                #print(params)
                url += f'?{params}'
                print(url)
            try:
                (response, content) = nam.request(url, blocking=True) # TODO Turn into non-blocking and QgsTask
            except RequestsException as e:
                print(f'exception: {e}')
                return
        #print('result:', nam.httpResult())

        #print('response: ', response)
        #print('content: ', content)
        print(response.status)
        #print(content)
        if response.status == 200:
            return content


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
