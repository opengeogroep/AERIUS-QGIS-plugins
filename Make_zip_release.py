import argparse
import zipfile
import pathlib

def add_to_zip(file_path):
    # Ignore test directory
    try:
        if file_path.parts[1] in ['test']:
            return False
    except(IndexError):
        pass

    # Ignore pycache
    patterns_to_ignore = ['*/__pycache__/*', '__pycache__']
    for pattern in patterns_to_ignore:
        if file_path.match(pattern):
            return False

    return True

parser = argparse.ArgumentParser()
parser.add_argument('version', help='Version number (e.g. 3.1.1)')
parser.add_argument('--verbose', help='Verbose output',  action='store_const', const=True)
args = parser.parse_args()

output_zip_file_name = f'ImaerPlugin-{args.version}.zip'
plugin_directory = pathlib.Path('ImaerPlugin')

with zipfile.ZipFile(output_zip_file_name, mode="w", compression=zipfile.ZIP_DEFLATED) as archive:
    for file_path in plugin_directory.rglob("*"):
        if add_to_zip(file_path):
            archive.write(pathlib.Path(file_path))
        else:
            if args.verbose:
                print(f'Skipping {file_path}')

print(f'Generated: {output_zip_file_name}')