import json
import urllib.parse

from .network import NetworkAccessManager, RequestsException




class AeriusConnection():

    def __init__(self, version=None, api_key=None):
        self.available_versions = ['6', '7']

        if version is None:
            version = self.available_versions[-1]
        else:
            version = str(version)
            #if self.version not in self.available_versions:
            #    pass # TODO: Throw some error?
        self.set_version(version)

        self.base_url = None
        self.api_key = api_key


    def __str__(self):
        return 'AeriusConnection[v{}, {}, {}]'.format(
            self.version,
            self.api_key,
            self.base_url
        )

    def set_version(self, version):
        self.version = version
        url_lookup = {
            '6': 'https://connect.aerius.nl/api/6',
            #'99': 'https://connect.aerius.nl/api2020-prerelease',
            '7': 'https://natuur-dev.aerius.nl/api',
            #'7': 'https://connect-masterclass.aerius.nl/api',
        }
        self.base_url = url_lookup[self.version]


    def is_valid(self, test_api_key=True, test_server=False):
        if self.base_url is None:
            return False
            print('No base url')
        if test_api_key:
            if self.api_key is None or len(self.api_key) != 32:
                print('No (valid) api key')
                return False
        if test_server:
            return self.server_is_up()
        return True


    def run_request(self, api_function, method, data=None, with_version=True):
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        if with_version:
            url = f'{self.base_url}/v{self.version}/{api_function}'
        else:
            url = f'{self.base_url}/{api_function}'

        print(url)

        nam = NetworkAccessManager()

        if method == 'POST':
            if data is not None:
                body = json.dumps(data)
                #print(body)
            try:
                (response, content) = nam.request(url, method='POST', headers=headers, body=body)
            except RequestsException as e:
                #print(f'exception: {e}')
                return

        elif method == 'GET':
            if data is not None:
                #print(data)
                params = urllib.parse.urlencode(data)
                #print(params)
                url += f'?{params}'
                print(url)
            try:
                (response, content) = nam.request(url, method='GET', headers=headers)
            except RequestsException as e:
                print(f'exception: {e}')
                return

        elif method == 'DELETE':
            if data is not None:
                print(data)
                params = urllib.parse.urlencode(data)
                print(params)
                url += f'?{params}'
                print(url)
            try:
                (response, content) = nam.request(url, method='DELETE', headers=headers)
            except RequestsException as e:
                print(f'exception: {e}')
                return

        print(response)
        print(response.status)
        print(content)
        if not response.status == 200:
            return
        if len(content) > 0:
            return json.loads(content)


    def server_is_up(self):
        end_points = {
            '6': 'actuator/health', # werkt niet
            '7': 'actuator/health'
        }
        end_point = end_points[self.version]
        response = self.run_request(end_point, 'GET', with_version=False)
        return response is not None


    def generate_api_key(self, email):
        if not self.is_valid(test_api_key=False):
            return
        end_points = {
            '6': 'generateAPIKey',
            '7': 'user/generateApiKey'
        }
        end_point = end_points[self.version]
        data = {'email': email}
        response = self.run_request(end_point, 'POST', data)
        if response is not None:
            print(f'gelukt! {response}')


    def status_jobs(self):
        end_points = {
            '6': 'status/jobs',
            '7': 'jobs'
        }
        end_point = end_points[self.version]
        data = {}
        data['apiKey'] = self.api_key

        response = self.run_request(end_point, 'GET', data)
        if response is not None:
            print(f'gelukt! {response}')
        return response


    def validate(self, gml_fn):
        print('validate')
        api_function = 'validate'
        data = {}
        data['strict'] = False
        data['validateAsPriorityProject'] = False

        data_object = {}
        data_object['contentType'] = 'TEXT'
        data_object['dataType'] = 'GML'
        with open(gml_fn) as gml_file:
            data_object['data'] = gml_file.read()
        #data_object['substance']

        data['dataObject'] = data_object
        #print(data)

        response = self.run_request(api_function, 'POST', data)
        if response is not None:
            print(f'gelukt! {response}')
        return response


    def calculate(self, gml_fn, user_options={}):
        print('calculate')
        api_function = 'calculate'

        data = {}
        data['apiKey'] = self.api_key

        options = {}
        options['calculationType'] = 'NBWET'
        options['year'] = 2020
        options['substances'] = ['NH3', 'NOX']
        #options['name'] = 'situatie1'
        #options['receptorSetName'] = 'vera'
        #options['stacking'] = True
        #options['aggregate'] = False
        #options['validate'] = True
        #options['range'] = 0
        #options['tempProjectYears'] = 0
        #options['permitCalculationRadiusType'] = 'NONE'
        #options['roadOPS'] = 'DEFAULT'
        #options['meteoYear'] = '2013'
        #options['sendEmail'] = True
        #options['useReceptorHeight'] = False

        options.update(user_options)

        output_options = {}
        output_options['resultTypes'] = ['DEPOSITION']
        output_options['sectorOutput'] = False
        output_options['outputType'] = 'GML'
        options['outputOptions'] = output_options

        data['options'] = options

        calc_data_objects = []

        calc_data_object = {}
        calc_data_object['contentType'] = 'TEXT'
        calc_data_object['dataType'] = 'GML'
        with open(gml_fn) as gml_file:
            calc_data_object['data'] = gml_file.read()
        #calc_data_object['substance'] = 'NH3'
        #calc_data_object['expectRcpHeight'] = False

        calc_data_objects.append(calc_data_object)

        data['calculateDataObjects'] = calc_data_objects

        data['strict'] = False

        response = self.run_request(api_function, 'POST', data)
        if response is not None:
            print(f'gelukt! {response}')

        return response


    def get_receptor_sets(self):
        api_function = 'receptorSets'
        data = {}
        data['apiKey'] = self.api_key

        response = self.run_request(api_function, 'GET', data)
        if response is not None:
            print(f'gelukt! {response}')
        return response


    def post_receptor_set(self, gml_fn, name, description=''):
        '''Posts a new receptor set'''
        print('receptor_set')
        api_function = 'receptorSet'

        data = {}
        data['apiKey'] = self.api_key
        data['name'] = name
        data['description'] = description

        data_object = {}
        data_object['contentType'] = 'TEXT'
        data_object['dataType'] = 'GML'
        with open(gml_fn) as gml_file:
            data_object['data'] = gml_file.read()
        #data_object['substance'] = 'NH3'
        #data_object['expectRcpHeight'] = False

        data['dataObject'] = data_object

        print(data)

        response = self.run_request(api_function, 'POST', data)
        if response is not None:
            print(f'gelukt! {response}')

        return response

    def delete_receptor_set(self, name):
        print('delete_receptor_set')
        api_function = f'receptorSet/{name}'
        data = {}
        data['apiKey'] = self.api_key

        response = self.run_request(api_function, 'DELETE', data)
        if response is not None:
            print(f'gelukt! {response}')

        return response
