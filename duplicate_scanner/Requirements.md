    -- Main menu --
Options:
1. Search duplicates
2. Map local address
3. Check back-up copies


    -- Search duplicates --
Input: path or a list of paths or Map object
If there is a single path, app searches for duplicates within this path.
If there are a list of paths, app searches for duplicates in all these paths.
If there are only Map objects, app searches for duplicates within this path and post searching activities will be limited.
If there is a mix of path and Map, user chose activity option.

Comparison criteria:
name, size, created, modified, hash.

Actions:
* Print results
* save results to txt.
* remove duplicates
* move duplicates to other folder (option for further development)

Removing/preserving duplicates according to defined criteria:
preserving criteria:
* last modified - default
* last created
* bigger size




    -- Map address --
Creates a list of MyFile objects and saves it on a disk or in DB.
This Map can be read in 'Check back-up copies'.


    -- Check back-up copies --
Input: a list of backup copies. a backup copy is a path or a Map.
Two options:
* Master copy vs backup copies
* equal copies

Master copy vs backup copies.
There can be only one master copy. In this case other copies are compared to master copy.
As the results there are two lists: missing files and extra files.

equal copies
There are exactly 2 copies. Result: 2 lists. Each list has 2 lists: missing files and extra files. 

There are 2 options for comparison.
* considering relative path
* regardless of relative path

considering relative path
Means that file of the backup copy must exist in the correct address. 
Otherwise, it is fixed in the list of missing or extra file.
Later those two list are checked and if file is in both lists - suggest to move it in correct place.

regardless of relative path
Relative positions of files are not important.
This can work only if there is no duplicates within each copy. 


    --Settings--
scan_ignore.txt:
list of folder
list of files
list fo file extensions