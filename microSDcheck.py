#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on Sat Sep 26 23:44:04 2015

@author: willy
"""

import random
import hashlib
import argparse
import shutil, os, time

def write_a_file(destination, character, size=1):
    """
    Create random file with specifyed size (in GBytes)
    and copy them to "destination". The file will be
    temporally created in the current folder, then we keep
    the md5 hash of the file and delete it.
    """
    
    #just a random number for the first line
    line1 = 20000000 - int(random.random()*10000000)
    with open(destination, 'w') as f:
        f.write('{}\n'.format(line1))
        number_of_characters = (1024**3)*size -10
        characters_to_write = character * number_of_characters
        f.write(characters_to_write)
    md5_value = md5sum(destination)
    return md5_value
    
def md5sum(filename, blocksize=65536):
    hash = hashlib.md5()
    with open(filename, "r+b") as f:
        for block in iter(lambda: f.read(blocksize), ""):
            hash.update(block)
    return hash.hexdigest()
    
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("microSDpath")
    parser.add_argument("-s", "--size", type=int, help="total size to test",
                        default=25)
                        
    args = parser.parse_args()
    original_md5_sums = []
    copied_md5_sums = []
    writing_time = 0
    reading_time = 0
    
    # writing the files of size 1GB in the current folder
    for i in range(1, args.size+1):
        current_dir = os.getcwd()
        newfilename = 'test_data_{}.data'.format(i)
        new_file_path = os.path.join(current_dir, newfilename)
        new_md5 = write_a_file(new_file_path, '0')
        original_md5_sums.append(new_md5)
        print('Created file {}'.format(i))
        # try to coppy to the microSDcard
        try:
            start = time.time()
            shutil.copy(new_file_path, args.microSDpath)
            end = time.time()
            writing_time += (end-start)
            print('File {} copied to the microSD card'.format(i))
        except:
            pass
        os.remove(new_file_path)
        
    # Get the md5 hash of the files in the microSD card
    for i in range(1, args.size+1):
        newfilename = 'test_data_{}.data'.format(i)
        copied_file_path = os.path.join(args.microSDpath, newfilename)
        start = time.time()
        copied_md5_sums.append(md5sum(copied_file_path))
        end = time.time()
        reading_time += (end-start)

    # writting final report
    results = []
    if len(original_md5_sums) != len(copied_md5_sums):
        d = len(original_md5_sums) - len(copied_md5_sums)
        results.append('There were {} files not copied'.format(d))
    m = min(len(original_md5_sums), len(copied_md5_sums))
    for i in range(m):
        if original_md5_sums[i] == copied_md5_sums[i]:
            line = '{}\t{}\tOK'.format(original_md5_sums[i], copied_md5_sums[i])
        else:
            line = '{}\t{}\tERROR'.format(original_md5_sums[i], copied_md5_sums[i])
        results.append(line)
    
    writting_speed = round(float(args.size*1024)/writing_time, 2)
    reading_speed = round(float(args.size*1024)/reading_time, 2)
    
    results.append("Writting speed {} MB/s".format(writting_speed))
    results.append("Read speed {} MB/s".format(reading_speed))
    
    with open(os.path.join(current_dir, 'results.txt'), 'w') as f:
        f.write('\n'.join(results))
        
    print('done\n{}'.format('\n'.join(results)))
