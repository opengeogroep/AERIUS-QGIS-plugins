import json
import urllib.parse
import time

import requests
#from qgis.PyQt.QtCore import

from qgis.core import (
    Qgis,
    QgsNetworkAccessManager,
    QgsBlockingNetworkRequest
)

from .network import NetworkAccessManager, RequestsException

from qgis.PyQt.QtCore import (
    QFile,
    QFileInfo,
    QIODevice,
    QVariant,
    QUrl
)
from qgis.PyQt.QtNetwork import (
    QHttpMultiPart,
    QHttpPart,
    QNetworkRequest
)




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
            #'7': 'https://natuur-dev.aerius.nl/api', # imaer 4
            '7': 'https://connect-masterclass.aerius.nl/api', # imaer 3
            #'7': 'http://localhost:5000', # imaer 3
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


    def run_multi_part_request(self, api_function, method, text_parts=[], file_parts=[], with_api_key=True, blocking=True):
        print('run_multi_part_request ------------------------------------------------')

        manager = QgsNetworkAccessManager.instance()

        url = f'{self.base_url}/v{self.version}/{api_function}'
        #url = 'http://localhost:5000' # echo server for debugging

        print(url)
        url = QUrl(url)
        print(url)
        request = QNetworkRequest(url)
        print(request)
        #if with_api_key:
        if with_api_key:
            print(f'adding_api_key {self.api_key}')
            request.setRawHeader(b'api-key', self.api_key.encode('utf-8'))
            #request.setRawHeader(b'api-key', b'8f545f15cc684368a3f38a605dfb0148')

        if method == 'POST':
            print(text_parts)
            print(file_parts)

            multi_part = QHttpMultiPart(QHttpMultiPart.FormDataType)

            for tp in text_parts:
                print(tp)
                header = tp['header']
                body = json.dumps(tp['body'])
                body = body.encode('utf-8')
                text_part = QHttpPart()
                text_part.setHeader(QNetworkRequest.ContentDispositionHeader, QVariant(f'form-data; name="{header}"'))
                text_part.setBody(body)
                multi_part.append(text_part)

            for fp in file_parts:
                print(fp)
                file = QFile(fp)
                print(QFileInfo(file).fileName())  # <= om de file name te achterhalen en te gebruiken in de dispostion header

                file_part = QHttpPart()
                file_part.setHeader(QNetworkRequest.ContentTypeHeader, QVariant("application/gml+xml"))
                # zo ziet het eruit in curl in de echo server:
                #Content-Disposition: form-data; name="filePart"; filename="AERIUS_bijlage_eigen_rekenpunten_2020.gml"
                file_part.setHeader(QNetworkRequest.ContentDispositionHeader,
                    QVariant(f'form-data; name="filePart"; filename="{QFileInfo(file).fileName()}"'))
                file.open(QIODevice.ReadOnly)
                file_part.setBodyDevice(file)
                file.setParent(multi_part) # we cannot delete the file now, so delete it with the multi_part
                multi_part.append(file_part)

                reply = manager.post(request, multi_part)
                multi_part.setParent(reply)
                return(reply)

        if method == 'GET':
            request.setRawHeader(b'Content-Type', b'application/json')

            qgis_request = QgsBlockingNetworkRequest()

            err = qgis_request.get(request, True)
            #print(err)

            if err > 0:
                #TODO: return error code or None or something...
                return None

            reply = qgis_request.reply()
            return reply.content()


        if method == 'DELETE':
            request.setRawHeader(b'Content-Type', b'application/json')

            #print(Qgis.QGIS_VERSION_INT)
            if Qgis.QGIS_VERSION_INT < 32000:
                # version 3.18 or lower
                reply = manager.deleteResource(request)
                print(reply)
            else:
                qgis_request = QgsBlockingNetworkRequest()
                err = qgis_request.deleteResource(request)
                print(err)

                if err > 0:
                    #TODO: return error code or None or something...
                    return None

                reply = qgis_request.reply()
                return reply.content()



    def run_request(self, api_function, method, data=None, files=None, with_version=True, with_api_key=True):
        print('run_request')
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'}
        if with_api_key:
            headers['api-key'] = self.api_key

        if with_version:
            url = f'{self.base_url}/v{self.version}/{api_function}'
        else:
            url = f'{self.base_url}/{api_function}'

        print(url)

        #return None # just jump out

        nam = NetworkAccessManager()

        if method == 'POST':
            if data is not None:
                body = json.dumps(data)
                #print(body)

                r = requests.post(url, files=files)
                return r.text
            try:
                (response, content) = nam.request(url, method='POST', headers=headers, files=files)#, body=body)
            except RequestsException as e:
                #print(f'exception: {e}')
                return

        elif method == 'GET':
            if data is not None:
                #print(data)
                params = urllib.parse.urlencode(data)
                #print(params)
                if self.version == '6':
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


    def get_jobs(self):
        end_points = {
            '7': 'jobs'
        }
        end_point = end_points[self.version]

        response = self.run_multi_part_request(end_point, 'GET')
        if response is None:
            return

        print(f'gelukt! {response}')
        result = json.loads(bytes(response))
        return result


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


    def post_calculate(self, gml_fn, user_options={}):
        print('post_calculate()')

        '''Posts a new receptor set'''
        print('receptor_set')
        end_points = {
            '7': 'wnb/calculate'
        }
        end_point = end_points[self.version]

        options = {}
        user_options['outputType'] = 'GML' # GML or PDF
        user_options['sendEmail'] = False
        # update default options with user options
        options.update(user_options)

        print(options)

        base_name = QFileInfo(gml_fn).fileName()
        print(base_name)

        text_parts = [
            {'header': 'options', 'body': options},
            {'header': 'files', 'body': {'fileName': base_name, 'situation': 'REFERENCE'}}
        ]


        file_parts = []
        file_parts.append(gml_fn)
        print(file_parts)


        response = self.run_multi_part_request(end_point, 'POST', text_parts=text_parts, file_parts=file_parts)
        print(response)
        resp = response
        if response is not None:
            print(f'gelukt! {response}')

        self.last_response = response

        return response


    def get_receptor_sets(self):
        'Returns a dictionary of receptor sets, or None in case of network errors'
        end_points = {
            '7': 'receptorSets'
        }
        end_point = end_points[self.version]
        data = {}

        #response = self.run_request(end_point, 'GET', data)
        response = self.run_multi_part_request(end_point, 'GET')

        if response is None:
            return

        print(f'gelukt! {response}')
        self.resp = response
        result = json.loads(bytes(response))
        return result


    def post_receptor_set(self, gml_fn, name, description=''):
        '''Posts a new receptor set'''
        print('receptor_set')
        end_points = {
            '7': 'receptorSets'
        }
        end_point = end_points[self.version]

        text_parts = [
            {'header': 'receptorSet', 'body': {'name': name, 'description': description,  'expectRcpHeight': False}},
        ]
        file_parts = []
        file_parts.append(gml_fn)
        print(file_parts)

        #response = self.run_request(end_point, 'POST')
        response = self.run_multi_part_request(end_point, 'POST', text_parts=text_parts, file_parts=file_parts)
        print(response)
        resp = response
        if response is not None:
            print(f'gelukt! {response}')

        self.last_response = response

        return response


    def delete_receptor_set(self, name):
        print('delete_receptor_sets')
        api_function = f'receptorSets/{name}'

        response = self.run_multi_part_request(api_function, 'DELETE')
        if response is not None:
            print(f'gelukt! {response}')

        return response
