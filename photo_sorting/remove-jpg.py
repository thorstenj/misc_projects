#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
Written on 2012-12-12 by Philipp Klaus <philipp.l.klaus →AT→ web.de>.
Check <https://gist.github.com/4271012> for newer versions.

Also check <https://gist.github.com/3155743> for a tool to
rename JPEGs according to their EXIF shot time.
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
    parser = argparse.ArgumentParser(description='Cleanup of leftover raw image files (*.CR2).')
    parser.add_argument('-n', '--no-backup', action='store_true',
            help='Don\'t backup orphaned raw images  -  delete them immediately.')
    parser.add_argument('-b', '--backup-folder', default='/Users/thorstenjaeckel/Cleanup',
            help='Folder to move orphaned raw images to.')
    parser.add_argument('-q', '--quiet', action='store_true',
            help='Silence the less important output of this tool.')
    parser.add_argument('folder', metavar='CHECK_FOLDER', default='./', nargs='?',
            help='Folder to check for raw images. Defaults to the current working directory')
    args = parser.parse_args()
    verbose = not args.quiet
    raw_images, jpeg_images_bare_names = [], []
    all_files = list(os.listdir(args.folder))
    # sort files into raw and jpeg files
    for filename in all_files:
        # The file name of raw image ends with .CR2 for Canon EOS cameras
        if re.match(r'(.*)\.[jJ][pP][eE]?[gG]$', filename):
            raw_images.append(filename)
        if re.match(r'(.*)\.[nN][eE][fF]$', filename):
            jpeg_images_bare_names.append(os.path.splitext(filename)[0])
    # Check if there is a jpeg for each raw image
    orphans = []
    for raw_image in raw_images:
        if os.path.splitext(raw_image)[0] not in jpeg_images_bare_names:
            orphans.append(raw_image)
    if len(raw_images) + len(jpeg_images_bare_names) == 0:
        if verbose: stderr("No images found. Are you sure you wanted to check '%s' for orphaned RAW images?" %
                (args.folder,))
        sys.exit(2)
    elif len(raw_images) == 0:
        if verbose: print "No RAW images found, but %i JPEGs. Won't do anything now." % (
                len(jpeg_images_bare_names),)
        sys.exit(0)
    elif len(orphans) == 0:
        if verbose: print "%i RAW images found, and %i JPEGs but no orphans. Won't do anything now." % (
                len(raw_images), len(jpeg_images_bare_names))
        sys.exit(0)
    backup_folder = None if args.no_backup else os.path.join(args.folder,args.backup_folder)
    delete([os.path.join(args.folder,orphan) for orphan in orphans], backup_folder=backup_folder, verbose=verbose)

