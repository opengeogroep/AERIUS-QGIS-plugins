import zipfile
import pathlib

release_no = 1234

folders_to_ignore = ['*\\test\\output\\*', '*\__pycache__\*', '*\\__pycache__']

output_zip_file_name = f'ImaerPlugin-{release_no}.zip'

directory = pathlib.Path('ImaerPlugin')
all_files = []
files_to_zip = []
with zipfile.ZipFile(output_zip_file_name, mode="w") as archive:
    for file_path in directory.rglob("*"):
        all_files.append(str(file_path)) # this is all the files in the folder
        for folder in folders_to_ignore:
            if file_path.match(folder) is True:
                files_to_zip.append(str(file_path)) # this is only the files in our folders to remove

    final_list_to_zip = (set(all_files) - set(files_to_zip))

    for file_name in final_list_to_zip:
        archive.write(pathlib.Path(file_name),arcname=pathlib.Path(file_name))
