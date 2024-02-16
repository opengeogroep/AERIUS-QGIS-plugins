import os.path

import imaer_document.ImaerDocument
from .metadata import AeriusCalculatorMetadata

idoc = ImaerDocument()
# print(idoc)

project = {'year': 2021, 'description': 'Bla bla bal'}
situation = {'name': 'Situatie 1', 'reference': 'abc123xyz789'}
calculation = {'type': 'PERMIT', 'substances': ['NH3', 'NOX'], 'result_types': ['DEPOSITION']}
version = {'aeriusVersion': 'QGIS PLUGIN', 'databaseVersion': ''}
md = AeriusCalculatorMetadata(project, situation, calculation, version)
idoc.metadata = md

fn = '/home/raymond/tmp/imaer_test.xml'
idoc.to_xml_file(fn)
