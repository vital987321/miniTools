__version__ = '0'
"""App asks the user to input address of a local directory.
    App looks for duplicate files (based on name).
    # App skips files for  which access is not granted (for example "read only" files).
    App checks nested folders.
"""

import os
import datetime


class Myfile:
    id: int
    name: str  # name with extension
    shortname: str  # name without extension
    address: str  # with file name
    directory: str  # without file name
    extension: str
    size: int
    # readonly: bool
    # system: bool
    created: str
    modified: str
    accessed: str
    # Class properties
    lastid = 0
    check_parameters = ['name', 'size']
    ignore_extensions = []

    def __init__(self, name, directory):
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

    def __repr__(self):
        return self.name

    def __getextension(self):
        if '.' in self.name:
            return self.name.split('.')[-1]
        return ''

    def __getshortname(self):
        if '.' in self.name:
            return self.name[:len(self.name) - len(self.extension) - 1]
        else:
            return self.name

    def getsortingkey(self):
        key = ''
        for parameter in Myfile.check_parameters:
            key += str(getattr(self, parameter))
        return key

    @classmethod
    def incrementid(cls):
        cls.lastid += 1
        return cls.lastid


# while True:
#     try:
#         userfolder = input('Enter full address of the folder: ')
#         os.listdir(userfolder)
#         break
#     except:
#         raise Exception('Folder is not found. Enter correct address.')

userfolder = r'C:\Users\velychko\Desktop\duptest'
myfiles = []
for root, dirs, files in os.walk(userfolder):
    for file in files:
        myfiles.append(Myfile(file, root))

sorted_files = sorted(myfiles, key=lambda x: x.getsortingkey())

duplicates = []
groupopen = False
isduplicate = False
for i in range(1, len(sorted_files)):
    for parameter in Myfile.check_parameters:
        if getattr(sorted_files[i], parameter) == getattr(sorted_files[i - 1], parameter):
            isduplicate = True
        else:
            isduplicate = False
            break
    if isduplicate:
        if groupopen:
            duplicates[-1].append(sorted_files[i])
        else:
            duplicates.append([])
            groupopen = True
            duplicates[-1].append(sorted_files[i - 1])
            duplicates[-1].append(sorted_files[i])
    else:
        groupopen = False

for l in duplicates:
    print(l)
