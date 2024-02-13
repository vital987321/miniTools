In version 0:
1. ~~Handle 'read only file'  exception.~~
2. ~~Check files after removal. Print how may were really removed.~~
3. ~~What happens if file is open?~~
4. ~~If file is already deleted/moved?~~
4. ~~consider splitting code into separate functions.~~
5. ~~Write description.~~
6. ~~check if directories exist~~
7. Add GUI
8. Redo it based on Classes. Use Class methods as a toogle to the working mode.
9. Add possibiliti to work with any amout od initial directories, including 1.
10. Work with nested folders.
11. Consider the mode of comparing 2 backup copies. Wich files are missing? Wha if those copies are on a different notconnected PCs?


Traceback (most recent call last):
  File ".....\duplicates_in_a_folder.py", line 140, in <module>
    myfiles.append(Myfile(file, root))
                   ^^^^^^^^^^^^^^^^^^
  File ".....\duplicates_in_a_folder.py", line 37, in __init__
    self.size = os.stat(self.address).st_size
                ^^^^^^^^^^^^^^^^^^^^^
FileNotFoundError: [WinError 3] Systém nemůže nalézt uvedenou cestu: '...\\My_Documents\\Ba...
