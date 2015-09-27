# microSDcheck
Check if a microSD really has the capacity that the system reports.

A way of checking if a microSD really has the capacity that system reports (or seller claim) is to copy some file(s)
on it. Then you compare the files with the original ones.
This is a simple python scripts that creates files of size 1GB in the local folder, then copy these files to the 
microSD. To save place, I delete the created 1GB file once it has been copied to the microSD and keep only a md5 hash
value of it. 
When all the files are copied to the microSD, I do a md5 sum for all files in the microSD and compare them with the
md5 values of the original files.
Also, the script computes writting and reading speed.

