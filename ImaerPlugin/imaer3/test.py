import os.path

from __init__ import *

idoc = ImaerDocument()
#print(idoc)

project = {'year': 2021, 'description': 'Bla bla bal'}
situation = {'name': 'Situatie 1', 'reference': 'abc123xyz789'}
calculation = {'type': 'PERMIT', 'substances': ['NH3', 'NOX'], 'resultType': 'DEPOSITION'}
version = {'aeriusVersion': 'QGIS PLUGIN', 'databaseVersion': ''}
md = AeriusCalculatorMetadata(project, situation, calculation, version)
idoc.metadata = md


fn = '/home/raymond/tmp/imaer_test.xml'
idoc.to_xml_file(fn)

pdefs = idoc.get_gui_nodes()
#print(pdefs)

print(pdefs.to_string())
