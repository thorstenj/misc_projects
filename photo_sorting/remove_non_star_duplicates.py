#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
Based on JPG/RAW sorting script by by Philipp Klaus <https://gist.github.com/4271012>

Modifications made on 2017-01-08 by Thorsten Jaeckel <https://github.com/thorstenj>
"""

import argparse, os, errno, re, shutil, sys, random

def stderr(line):
    sys.stderr.write(line + '\n')
    sys.stderr.flush()

def delete(files, backup_folder=None, verbose=True):
    if len(files) == 0: return
    if backup_folder:
        try:
            os.mkdir(backup_folder)
        except OSError, e:
            if not e.errno == errno.EEXIST:
                raise
        for filename in files:
            if verbose: print "Moving %s to %s." % (filename, backup_folder)
            if os.path.isfile(os.path.join(backup_folder, filename)):
                x = random.randint(0,1000)
                new_file = filename + '_' + str(x)

                shutil.move(filename, new_file)
                shutil.move(new_file, os.path.join(backup_folder))
            else:
                shutil.move(filename, os.path.join(backup_folder))
    else:
        for filename in files:
            if verbose: print "Deleting %s." % (filename,)
            os.remove(filename)

if __name__ == '__main__':
    starred_images, jpeg_images_bare_names = [], []
    all_files = list(os.listdir('./'))

    # sort files 
    for filename in all_files:
        # Create list of all starred files
        if re.match(r'Stars', os.path.splitext(filename)[0][1:]):
            starred_images.append(os.path.splitext(filename)[0])
        # Create list of all JPG files in folder
        if re.match(r'(.*)\.[jJ][pP][gG]$', filename):
            jpeg_images_bare_names.append(os.path.splitext(filename)[0])

    # Check of there is a regular JPG for a starred file in the folder
    to_delete = []
    for starred_image in starred_images:
        if re.split('Stars-',starred_image[1:])[1] in jpeg_images_bare_names:
            file_to_remove = re.split('Stars-',starred_image[1:])[1] + '.JPG'
            print "Starred image '%s' found - removing original image" % starred_image
            to_delete.append(file_to_remove)
    if len(starred_images) + len(jpeg_images_bare_names) == 0:
        stderr("No images found. Are you sure you wanted to check '%s' for orphaned RAW images?" %
        ('./',))
        sys.exit(2)
    elif len(starred_images) == 0:
        print "No RAW images found, but %i JPEGs. Won't do anything now." % (
        len(jpeg_images_bare_names),)
        sys.exit(0)
    elif len(to_delete) == 0:
        print "%i RAW images found, and %i JPEGs but no orphans. Won't do anything now." % (
        len(starred_images), len(jpeg_images_bare_names))
        sys.exit(0)
    backup_folder = os.path.join('./','/Users/thorstenjaeckel/Cleanup')
    delete([os.path.join('./',delete) for delete in to_delete], backup_folder=backup_folder)

