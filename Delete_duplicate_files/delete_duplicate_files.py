__version__='0'

import os

def deletefiles(folder:str, flist:list[str]):
    nopermission_files = []
    deleted = 0
    notFoundFiles=[]
    for file in flist:
        try:
            os.remove(os.path.join(folder, file))
            deleted += 1
        except PermissionError:
            nopermission_files.append(file)
        except FileNotFoundError:
            notFoundFiles.append(file)
    return {'deleted': deleted,
            'nopermission_files': nopermission_files,
            'notFoundFiles': notFoundFiles}

while True:
    folder1=input('Enter full address of folder 1: ')
    folder2=input('Enter full address of folder 2: ')
    if folder1==folder2:
        print('folder 1 and folder 2 must be different.')
    else:
        break

files1 = [f for f in os.listdir(folder1) if os.path.isfile(os.path.join(folder1,f))]
files2 = [f for f in os.listdir(folder2) if os.path.isfile(os.path.join(folder2,f))]
duplicates=[]
for file in files1:
    if file in files2:
        duplicates.append(file)

if len(duplicates)>0:
    print(f'{len(duplicates)} duplicate(s) found:')
    for file in duplicates:
        print(file)
    isdelete=input(f'\n!!! Do you want to delete these files from {folder1} ? (y/n): ')
    if isdelete.lower()=='y':
        deleted=deletefiles(folder1,duplicates)
        if deleted['nopermission_files']:
            print('\nThe following files can not be deleted:')
            for file in deleted['nopermission_files']:
                print(file)
        if deleted['notFoundFiles']:
            print(f"\n{len(deleted['notFoundFiles'])} file(s) have not been found.")
        print (f"\n{deleted['deleted']} files deleted.")
    else:
        print('Files are not deleted.')
else:
    print('Nothing is deleted.')



