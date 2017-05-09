# microSDcheck
Check if an SD memory really has the capacity that the system reports.

A way of checking if an SD memory really has the capacity that system reports (or the seller claims) is to copy some file(s)
on it. Then compare the copied files with the original ones.
This is a simple python script that creates files of size 1GB in the local folder, then copy these files to the
SD card. To save place, I delete the created 1GB file once it has been copied to the SD card and keep only the md5 hash
value of it.
When all the files are copied to the SD card, I do a md5 sum for each file in the SD card and compare them with the
md5 values of the original files.
Also, the script computes writing and reading speed.
