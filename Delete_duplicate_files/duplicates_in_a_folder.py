__version__ = '0'
""" App looks for duplicate files in an inputted folder and nested folders.
    App asks the user to input address of a local directory.
    App looks for duplicate files based on specified parameters.
        Parameters by default are file name and file size.
    App asks if duplicates shall be deleted. 
"""

import os
import datetime


# --------------------- Classes ---------------------
class Myfile:
    id: int
    name: str  # name with extension
    shortname: str  # name without extension
    address: str  # with file name
    directory: str  # without file name
    extension: str
    size: int
    created: str
    modified: str
    accessed: str

    # Class properties
    __last_id = 0
    check_parameters = ['name', 'size']  # recommended ['name', 'size']
    ignore_extensions = []  # for example: 'mp3', 'sys'
    criteria = 'modified'  # criteria for preserving copy

    def __init__(self, name: str, directory: str):
        self.id = Myfile.increment_id()
        self.name = name
        self.directory = directory
        self.address = os.path.join(self.directory, self.name)
        self.size = os.stat(self.address).st_size
        self.extension = self.__getextension()
        self.shortname = self.__getshortname()
        self.created = datetime.datetime.fromtimestamp(os.stat(self.address).st_ctime).strftime('%Y-%m-%d %H:%M')
        self.accessed = datetime.datetime.fromtimestamp(os.stat(self.address).st_atime).strftime('%Y-%m-%d %H:%M')
        self.modified = datetime.datetime.fromtimestamp(os.stat(self.address).st_mtime).strftime('%Y-%m-%d %H:%M')

    def __repr__(self) -> str:
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

    def get_sorting_key(self) -> str:
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
    def increment_id(cls) -> int:
        cls.__last_id += 1
        return cls.__last_id


# --------------------- Functions ---------------------
def show_duplicates(duplicates, export_to_file=False):
    result = ''
    for group in duplicates:
        result += f'\n{len(group)} copies of file {group[0].name}:\n'
        for file in group:
            result += (f'\t{file.name},\t{file.directory}\n')
    if export_to_file:
        with open(os.path.join(user_folder, 'duplicates.txt'), "w") as output:
            output.write(result)
        print(f'Results are written to file {os.path.join(user_folder, "duplicates.txt")}')
    else:
        print(result)


def delete_duplicates(duplicates, export_to_file=False):
    deleted_files = {'deleted': [], 'no_permission': [], 'not_found': []}
    for group in duplicates:
        group.sort(key=lambda x: x.modified)
        for i in range(len(group) - 1):
            delstatus = group[i].delete()
            deleted_files[delstatus].append(group[i])
    report(deleted_files, export_to_file)


def report(deleted_files, export_to_file):
    report = ''
    if deleted_files["deleted"]:
        report += f'Deleted files ( total: {len(deleted_files["deleted"])}):\n'
        for file in deleted_files["deleted"]:
            report += f'\t{file.name}\t{file.directory}\n'
    if deleted_files['no_permission']:
        report += f'Files without permission to delete ( total: {len(deleted_files["no_permission"])}):\n'
        for file in deleted_files["no_permission"]:
            report += f'\t{file.name}\t{file.directory}\n'
    if deleted_files['not_found']:
        report += f'The following files are not found ( total: {len(deleted_files["not_found"])}):\n'
        for file in deleted_files["not_found"]:
            report += f'\t{file.name}\t{file.directory}\n'
    if export_to_file:
        with open(os.path.join(user_folder, 'deletion_report.txt'), "w") as output:
            output.write(report)
            print(f'Results logged to file {os.path.join(user_folder, "deletion_report.txt")}')
    else:
        print(report)


# --------------------- Main boby ---------------------
while True:
    try:
        user_folder = input('Enter full address of the folder: ')
        os.listdir(user_folder)
        break
    except:
        raise Exception('Folder is not found. Enter correct address.')


# Making a list of all files in the directory
myfiles = []
for root, dirs, files in os.walk(user_folder):
    for file in files:
        myfiles.append(Myfile(file, root))

# Sorting files list
myfiles = sorted(myfiles, key=lambda x: x.get_sorting_key())

# Making a list of groups of duplicates
duplicates = []
group_open = False
isduplicate = False
for i in range(1, len(myfiles)):
    if myfiles[i].extension in Myfile.ignore_extensions:
        group_open = False
        continue

    for parameter in Myfile.check_parameters:
        if getattr(myfiles[i], parameter) == getattr(myfiles[i - 1], parameter):
            isduplicate = True
        else:
            isduplicate = False
            break
    if isduplicate:
        if group_open:
            duplicates[-1].append(myfiles[i])
        else:
            duplicates.append([])
            group_open = True
            duplicates[-1].append(myfiles[i - 1])
            duplicates[-1].append(myfiles[i])
    else:
        group_open = False

# what to do with duplicates?
if duplicates:
    user_choice = input('\n---------------- ? ----------------\n'
                       'Select what shell be done with duplicates:\n'
                       '\t1 - show in console.\n'
                       '\t2 - save to file.\n'
                       '\t3 - delete and report to console.\n'
                       '\t4 - delete and report to file.\n'
                       '\t\tUser choice: ')
    if user_choice == '1':
        show_duplicates(duplicates)
    elif user_choice == '2':
        show_duplicates(duplicates, export_to_file=True)
    elif user_choice == '3':
        delete_duplicates(duplicates)
    elif user_choice == '4':
        delete_duplicates(duplicates, export_to_file=True)
else:
    print('No duplicates found.')

