__version__ = '0'
""" App looks for duplicate files in an inputted and nested folders.
    App asks the user to input address of a local directory.
    App looks for duplicate files based on specified parameters.
        Parameters by default are file name and file size.
    App writes to file the list of found duplicates. 
"""

import os
import datetime


class Myfile:
    id: int
    name: str           # name with extension
    shortname: str      # name without extension
    address: str        # with file name
    directory: str      # without file name
    extension: str
    size: int
    # readonly: bool
    # system: bool
    created: str
    modified: str
    accessed: str

    # Class properties
    __last_id = 0
    check_parameters = ['name', 'size']     # recommended ['name', 'size']
    ignore_extensions = []                  # for example: 'mp3', 'sys'
    criteria='modified'                     # criteria for preserving copy

    def __init__(self, name:str, directory: str):
        self.id = Myfile.incrementid()
        self.name = name
        self.directory = directory
        self.address = os.path.join(self.directory, self.name)
        self.size = os.stat(self.address).st_size
        self.extension = self.__getextension()
        self.shortname = self.__getshortname()
        self.created = datetime.datetime.fromtimestamp(os.stat(self.address).st_ctime).strftime('%Y-%m-%d %H:%M')
        self.accessed = datetime.datetime.fromtimestamp(os.stat(self.address).st_atime).strftime('%Y-%m-%d %H:%M')
        self.modified = datetime.datetime.fromtimestamp(os.stat(self.address).st_mtime).strftime('%Y-%m-%d %H:%M')

    def __repr__(self)->str:
        return self.name

    def __getextension(self) -> str:
        if '.' in self.name:
            return self.name.split('.')[-1]
        return ''

    def __getshortname(self) -> str:
        if '.' in self.name:
            return self.name[:len(self.name) - len(self.extension) - 1]
        else:
            return self.name

    def getsortingkey(self) -> str:
        key = ''
        for parameter in Myfile.check_parameters:
            key += str(getattr(self, parameter))
        return key

    def delete(self):
        try:
            os.remove(self.address)
            return 'deleted'
        except PermissionError:
            return 'no_permission'
        except FileNotFoundError:
            return 'not_found'

    @classmethod
    def incrementid(cls) -> int:
        cls.__last_id += 1
        return cls.__last_id


class FilesGroup:
    files:list[Myfile]
    def __int__(self, files:tuple[Myfile]=()):
        self.files=list(files)

    def append(self, myfile:Myfile):
        self.files.append(myfile)

    @classmethod
    def getfolderfiles(cls, directory: str):
        allfiles=[]
        for root, dirs, files in os.walk(directory):
            for file in files:
                allfiles.append(Myfile(file, root))
        return cls(allfiles)





# while True:
#     try:
#         userfolder = input('Enter full address of the folder: ')
#         os.listdir(userfolder)
#         break
#     except:
#         raise Exception('Folder is not found. Enter correct address.')

userfolder = r'C:\Users\velychko\Desktop\dt'

# Making a group with all files in the directory
allfiles=FilesGroup.getfolderfiles(userfolder)

# Sorting files list










# old approach
#######################

def report(deletedfiles, directory:str=''):
    report =f'Number of deleted files: {len(deletedfiles["deleted"])}\n'
    if deletedfiles['no_permission']:
        report+=f'Files without permission to delete ( total: {len(deletedfiles["no_permission"])}):\n'
        for file in deletedfiles["no_permission"]:
            report+=f'\t{file.name}\t{file.directory}'
    if deletedfiles['not_found']:
        report+=f'The following files are not found ( total: {len(deletedfiles["not_found"])}):\n'
        for file in deletedfiles["not_found"]:
            report+=f'\t{file.name}\t{file.directory}'
    if not directory:
            print (report)
    else:
        with open(os.path.join(directory, 'deletion_report.txt'), "w") as output:
            output.write(report)



# Making a list of all files in the directory
myfiles = []
for root, dirs, files in os.walk(userfolder):
    for file in files:
        myfiles.append(Myfile(file, root))

# Sorting files list
myfiles = sorted(myfiles, key=lambda x: x.getsortingkey())

# Making a list of groups of duplicates
duplicates = []
groupopen = False
isduplicate = False
for i in range(1, len(myfiles)):
    if myfiles[i].extension in Myfile.ignore_extensions:
        groupopen = False
        continue

    for parameter in Myfile.check_parameters:
        if getattr(myfiles[i], parameter) == getattr(myfiles[i - 1], parameter):
            isduplicate = True
        else:
            isduplicate = False
            break
    if isduplicate:
        if groupopen:
            duplicates[-1].append(myfiles[i])
        else:
            duplicates.append([])
            groupopen = True
            duplicates[-1].append(myfiles[i - 1])
            duplicates[-1].append(myfiles[i])
    else:
        groupopen = False

# what to do with duplicates?
if duplicates:
    userchoice = input('\n---------------- ? ----------------\n'
                       'Select what shell be done with duplicates:\n'
                       '\t1 - show in console.\n'
                       '\t2 - save to file.\n'
                       '\t3 - delete and report to console.\n'
                       '\t4 - delete and report to file.\n'
                       '\t\tUser choice: ')

else:
    print('No duplicates found.')

# writing list of duplicates to file
# with open(os.path.join(userfolder, 'duplicates.txt'), "w") as output:
#     if duplicates:
#         for group in duplicates:
#             output.write(f'\n{len(group)} copies of file {group[0].name}:\n')
#             for file in group:
#                 output.write(f'\t{file.name},\t{file.directory}\n')
#         print(f'Results are written to file {os.path.join(userfolder, "duplicates.txt")}')
#     else:
#         print('No duplicates found.')

# test
if duplicates:
    for group in duplicates:
        print(f'\n{len(group)} copies of file {group[0].name}:\n')
        for file in group:
            print(f'\t{file.name},\t{file.directory},\t{file.modified}\n')
else:
    print('No duplicates found.')

#removing duplicates
if duplicates:
    deletedfiles={'deleted':[], 'no_permission':[], 'not_found':[]}
    for group in duplicates:
        group.sort(key=lambda x: x.modified)
        for i in range(len(group)-1):
            delstatus=group[i].delete()
            deletedfiles[delstatus].append(group[i])
    report(deletedfiles)
else:
    print('No duplicates found.')






