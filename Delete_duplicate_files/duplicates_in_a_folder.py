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

    def __init__(self, name, directory):
        self.name = name
        self.directory = directory
        self.address = os.path.join(self.directory, self.name)
        self.size = os.stat(self.address).st_size
        self.extension = self.__getextension()
        self.shortname = self.__getshortname()
        self.created = datetime.datetime.fromtimestamp(os.stat(self.address).st_ctime).strftime('%Y-%m-%d %H:%M')
        self.accessed = datetime.datetime.fromtimestamp(os.stat(self.address).st_atime).strftime('%Y-%m-%d %H:%M')
        self.modified = datetime.datetime.fromtimestamp(os.stat(self.address).st_mtime).strftime('%Y-%m-%d %H:%M')

    def __getextension(self):
        if '.' in self.name:
            return self.name.split('.')[-1]
        return ''

    def __getshortname(self):
        if '.' in self.name:
            return self.name[:len(self.name) - len(self.extension) - 1]
        else:
            return self.name


# while True:
#     try:
#         userfolder = input('Enter full address of the folder: ')
#         os.listdir(userfolder)
#         break
#     except:
#         raise Exception('Folder is not found. Enter correct address.')

userfolder = 'D:\git\miniTools'
myfiles = []
for root, dirs, files in os.walk(userfolder):
    for file in files:
        # print(os.path.join(root, file))
        print(os.stat(os.path.join(root, file)).st_size)
        myfiles.append(Myfile(file, root))

for f in myfiles:
    print(f.name, f.shortname, f.extension, f.size, f.address)
    # print(type(f.created))
