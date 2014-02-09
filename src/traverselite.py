#! usr/bin/env python3.3
"""
traverselite.py
by Hawk Weisman
for CMPSC440 at Allegheny College

A lightweight version of traverse.py that shouldn't require
any external libraries, allowing it to be run on any system 
with Python installed.

Usage: 
	python traverselite.py 	(DIRECTORY) [--size] [--links] [--verbose] [--csv]

Arguments:
	DIRECTORY 				Root directory from which to begin traversal.

Options:
	--verbose				Verbose mode execution
	--size					Analyze file size
	--links  				Analyze file link count
	--csv 					Output a CSV

"""

import os, csv, time, datetime, bz2
from sys import argv, platform
from stat import *

def makecsv(directory,filesystem,traversetime):

	timestamp = datetime.datetime.now()
	filename = directory[1:].replace('/', '-') + "_" + str(timestamp.strftime('%Y-%m-%d')) + ".csv.bz2"

	with bz2.BZ2File("data/" + filename, 'wb') as f:
		writer = csv.writer(f)
		writer.writerow(['path', 'st_mode', 'st_ino', 'st_dev', 'st_nlink',
						 'st_uid', 'st_gid', 'st_size', 'st_atime', 'st_mtime',
						 'st_ctime'])
		for key, value in filesystem.items():
			writer.writerow([key, value. st_mode,
			                value.st_ino,  value.st_dev, value.st_nlink, 
			                value.st_uid, value.st_gid, value.st_size, 
			                value.st_atime, value.st_mtime, value.st_ctime])
		f.close();

	if '--nometadata' not in argv:

			metadata = "data/datafiles.csv"

			with open(metadata, 'a') as m:
				writer = csv.writer(m)
				writer.writerow([filename, timestamp, platform, traversetime, "", ""])

			m.close()

def main():
	"""Main function for traverselite"""
	directory = argv[1]

	start = time.clock()

	filesystem = traverse(directory)

	end = time.clock()

	print("Filesystem traversed in {:06} seconds\n".format(end - start))

	if '--csv' in argv:
		makecsv(directory,filesystem, end - start)

	if '--size' in argv:
		size(filesystem)

	if '--links' in argv:
		links(filesystem)


def mean(l):
	"""Returns the arithmetic mean of list l, as a float"""
	return sum(l) / len(l)

def traverse(path):
	"""Traverses the filesystem starting at path"""
	filesystem = {}
	_traverse(path,filesystem)
	return filesystem

def _traverse(path, files):
	"""Helper traversal function"""

	for item in os.listdir(path):

		# get the path to the current item
		itempath = os.path.join(path, item)	

		if '--verbose' in argv:
			print(itempath)
		
		# os.lstat() does not follow symlinks; we are not 
		try:
			files[itempath] = os.lstat(itempath)											
		except IOError:								
			print("failed to get information about %s, IOError" % itempath)
			files[itempath] = "IOERROR"
		except OSError:								
			print("failed to get information about %s, OSError" % itempath)
			files[itempath] = "OSERROR"
		else:
			# check if the stat-ed item is a directory, and if it is, recurse
			if S_ISDIR(files[itempath].st_mode):
				_traverse(itempath,files)			

def size(filesystem):
	"""Perform analyses related to file size"""

	# exclude 0-byte items: those are directories.
	bytesizes = [value.st_size for value in filesystem.values() if value.st_size > 0]
	kbsizes = [n/1024 for n in bytesizes] 

	if sys.argv.contains('--verbose'):
		for value in sorted(bytesizes):
			print("Found a %s file" % filesize(value))

	print("Average file size:\t{0}kB\t({1} files)".format(mean(kbsizes), kbsizes.count(mean(kbsizes))))
	print("Maximum file size:\t{0}kB\t({1} files)".format(max(kbsizs), kbsizes.count(max(kbsizes))))
	print("Minimum file size:\t{0}kB\t({1} files)\n".format(min(kbsizes), kbsizes.count(min(kbsizes))))

def links(filesystem):
	"""Perform analyses related to file link count"""
	linkcount = []

	for key, value in filesystem.items():
		linkcount.append(value.st_nlink)

	print("Average link count:\t{0}\t({1} files)".format(mean(linkcount), linkcount.count(mean(linkcount))))
	print("Maximum link count:\t{0}\t({1} files)".format(max(linkcount), linkcount.count(max(linkcount))))
	print("Minimum link count:\t{0}\t({1} files)\n".format(min(linkcount),linkcount.count(min(linkcount))))

if __name__ == '__main__':
	main()


 
