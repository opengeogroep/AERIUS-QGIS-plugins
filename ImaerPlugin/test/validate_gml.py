import sys
import os.path
import yaml
import json
import argparse

from importlib.machinery import SourceFileLoader

# Get settings for local dev
with open('dev.yml') as file:
    try:
        dev_config = yaml.safe_load(file)
        # print(dev_config)
    except yaml.YAMLError as exc:
        print(exc)
sys.path.append(dev_config['path_qgis_python_folder'])

from qgis.core import *

connect = SourceFileLoader("connect", "../connect/__init__.py").load_module()

# Parse cli argument(s)
parser = argparse.ArgumentParser(description='Check validity of GML file')
parser.add_argument('--dev', action='store_true', help='Run in developer mode')
parser.add_argument('gml_file', type=argparse.FileType(mode='r'), help='GML file to check')
args = parser.parse_args()
gml_fn = args.gml_file.name
# print(gml_fn)
# print(args.dev)

QgsApplication.setPrefixPath(dev_config['path_qgis_python_folder'], True)
qgs = QgsApplication([], True)
qgs.initQgis()

connect_base_url = dev_config['connect_base_url']
connect_version = dev_config['connect_version']
connect_key = dev_config['connect_key']
aerius_connection = connect.AeriusConnection(None, base_url=connect_base_url, version=connect_version, api_key=connect_key)
if args.dev:
    aerius_connection.dev = 'dev'
# print(aerius_connection)

result = aerius_connection.post_validate(gml_fn)
# print(result)
bstr = result.readAll()
# print(bstr)

try:
    result_dict = json.loads(bytes(bstr))
    # print(result_dict)
except:
    print('Server error, no validation response.')
    msg_box.exec()

print(f'--- {gml_fn} ---')
# print(result_dict)

if 'successful' in result_dict:
    print('successful: {}'.format(result_dict['successful']))
if 'errors' in result_dict and len(result_dict['errors']):
    print('errors:')
    for error in result_dict['errors']:
        code = error.get('code', 'unknown')
        message = error.get('message', 'unknown')
        print(f'  {message} ({code})')
if 'warnings' in result_dict and len(result_dict['warnings']):
    print('warnings:')
    for warning in result_dict['warnings']:
        code = warning.get('code', 'unknown')
        message = warning.get('message', 'unknown')
        print(f'  ({code}) {message}')
print('---')

qgs.exitQgis()
