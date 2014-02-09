#! usr/bin/env python3.3
"""
traverse.py
by Hawk Weisman
for CMPSC440 at Allegheny College

Tool to recursively traverse a filesystem and collect data on 
characteristics such as size, age, et cetera.

Usage: 
	traverse.py (DIRECTORY) [-slcha] [--size] [--links] [--histogram] [--verbose] [--csv] [--nometadata]

Arguments:
	DIRECTORY 			Root directory from which to begin traversal.

Options:
 	-h --help     		Show this screen.
	--histogram 		Make a histogram
	--verbose			Verbose mode execution
	-s, --size			Analyze file size
	-a, --age			Analyze file age
	-l, --links  		Analyze file link count
	-c, --csv 			Output a CSV
	--nometadata 		Do not collect and log metadata to datafiles.csv

"""

import os, numpy, math, csv, time, datetime, seaborn, matplotlib
from hurry.filesize import size as filesize
from scipy import stats
from matplotlib import pyplot, mlab
from docopt import docopt
from stat import *

def mean(l):
	"""Returns the arithmetic mean of list l, as a float"""
	return sum(l) / len(l)

def histogram(dataset, xlabel, title):

		seaborn.set_color_palette("deep", desat=.6)
		matplotlib.rc("figure", figsize=(8, 4))
		#seaborn.distplot(dataset)

		density = stats.gaussian_kde(dataset)
		density.covariance_factor = lambda : .25
		density._compute_covariance()

		xgrid = numpy.linspace(min(dataset), max(dataset), 100)
		pyplot.hist(dataset, bins=100, log=True)
		#pyplot.plot(xgrid, density.evaluate(xgrid), label='kde', color='r')
		#pyplot.plot(xgrid, stats.norm.pdf(xgrid), label='DGP normal', color="g")

		pyplot.xlabel(xlabel)
		pyplot.ylabel('Frequency (logarithmic)')
		pyplot.title(title)

		pyplot.show()

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

		if arguments['--verbose']:
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

	if arguments['--verbose']:
		for value in sorted(bytesizes):
			print("Found a %s file" % filesize(value))

	print("Average file size:\t{0}\t({1} files)".format(filesize(mean(bytesizes)), bytesizes.count(mean(bytesizes))))
	print("Maximum file size:\t{0}\t({1} files)".format(filesize(max(bytesizes)), bytesizes.count(max(bytesizes))))
	print("Minimum file size:\t{0}\t({1} files)\n".format(filesize(min(bytesizes)), bytesizes.count(min(bytesizes))))

	if arguments['--histogram']:
		histogram(kbsizes, 'File size in kB', 'Histogram of file sizes in tree starting at %s' % arguments["DIRECTORY"])
		#seaborn.distplot(kbsizes)

def links(filesystem):
	"""Perform analyses related to file link count"""
	linkcount = []

	for key, value in filesystem.items():
		linkcount.append(value.st_nlink)

	print("Average link count:\t{0}\t({1} files)".format(mean(linkcount), linkcount.count(mean(linkcount))))
	print("Maximum link count:\t{0}\t({1} files)".format(max(linkcount), linkcount.count(max(linkcount))))
	print("Minimum link count:\t{0}\t({1} files)\n".format(min(linkcount),linkcount.count(min(linkcount))))

	if arguments['--histogram']:
		histogram(linkcount, 'Number of links', 'Histogram of link frequency in tree starting at %s' % arguments["DIRECTORY"])

if __name__ == '__main__':
	arguments = docopt(__doc__, version='traverse.py 0.2')

	start = time.clock()

	filesystem = traverse(arguments["DIRECTORY"])

	end = time.clock()

	print("Filesystem traversed in {:06} seconds\n".format(end - start))

	if arguments['--csv']:

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

	if not arguments['--nometadata']:

			metadata = "data/datafiles.csv"

			with open(metadata, 'a') as m:
				writer = csv.writer(m)
				writer.writerow([filename, timestamp, platform, end-start, "", ""])

			m.close()

	if arguments['--size']:
		size(filesystem)

	if arguments['--links']:
		links(filesystem)

 