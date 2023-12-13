__version__='0'

import os
folder1=input('Enter full address of folder 1: ')
folder2=input('Enter full address of folder 2: ')

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
        for file in duplicates:
            os.remove(os.path.join(folder1,file))
        print(f'{len(duplicates)} file(s) deleted.')
    else:
        print('Files are not deleted.')
else:
    print('No duplicates found.')
