__version__ = '0'
"""App ask the user to input addresses of two local directories.
    App looks for duplicate files (based on name).
    App removes duplicate files from the first directory.
    App skips files for  which access is not granted (for example "read only" files).
    App does not check nested folders.
"""

import os


def deletefiles(folder: str, flist: list[str])->dict:
    """ Function deletes files from local address.
        Parameters:
            folder - str - address to a local directory where files to be deleted.
            flist - list[str] - list of files names with extensions to be deleted.
        Function skip files for  which access is not granted (for example "read only" files)
        Function returns a dictionary:
            {'deleted': deleted,                        # list of delete files
            'nopermission_files': nopermission_files,   # lisf of files skipped due permission error
            'notFoundFiles': notFoundFiles}             # list of files that were not found
            """
    nopermission_files = []
    deleted = []
    notFoundFiles = []
    for file in flist:
        try:
            os.remove(os.path.join(folder, file))
            deleted.append(file)
        except PermissionError:
            nopermission_files.append(file)
        except FileNotFoundError:
            notFoundFiles.append(file)
    return {'deleted': deleted,
            'nopermission_files': nopermission_files,
            'notFoundFiles': notFoundFiles}

# Main code
# Set two directories
while True:
    try:
        folder1 = input('Enter full address of folder 1: ')
        try:
            os.listdir(folder1)
        except:
            raise Exception('Folder 1 is not found')

        folder2 = input('Enter full address of folder 2: ')
        try:
            os.listdir(folder2)
        except:
            raise Exception('Folder 2 is not found')

        if folder1 == folder2:
            print('folder 1 and folder 2 must be different.')
    except Exception as ex:
        print (f'{ex}. Enter correct address.')
    else:
        break

# Read a list of files from both directories
files1 = [f for f in os.listdir(folder1) if os.path.isfile(os.path.join(folder1, f))]
files2 = [f for f in os.listdir(folder2) if os.path.isfile(os.path.join(folder2, f))]

# find duplicate files
duplicates = []
for file in files1:
    if file in files2:
        duplicates.append(file)

# Remove duplicate files and report.
if duplicates:
    print(f'{len(duplicates)} duplicate(s) found:')
    for file in duplicates:
        print(file)
    isdelete = input(f'\n!!! Do you want to DELETE these files from {folder1} ? (y/n): ')
    if isdelete.lower() == 'y':
        deleted = deletefiles(folder1, duplicates)
        if deleted['nopermission_files']:
            print('\nThe following files can not be deleted:')
            for file in deleted['nopermission_files']:
                print(file)
        if deleted['notFoundFiles']:
            print(f"\n{len(deleted['notFoundFiles'])} file(s) have not been found.")
        print(f"\n{len(deleted['deleted'])} file(s) deleted.")
    else:
        print('Files are not deleted.')
else:
    print('\nNo duplicates found.')
