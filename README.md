traverse
========

Doing science with filesystem traversal!

### What's Going On Here?

The `src/` directory in this repository contains two python scripts: `traverse.py` and `traverselite.py`, both of which recursively traverse a filesystem and collect data. `traverse.py` requires some additional Python libraries, including `numpy`, `scipy`, `matplotlib`, and `docopt`, which are not bundled with all Python installs and may not be available on all systems, such as Alden Hall lab computers. Therefore, I've bundled an additional script, `traverselite.py`, which will do data collection and output CSV files (as well as text to the console) without using the data analysis and graphing features provided by those libraries. However, if you do have these libraries installed or are willing to install them, the full-featured `traverse.py` will give you access to histograms of filesystem density and to a more usable command-line interface.

The `requirements.txt` file is for `traverse.py` -- `traverselite.py` can be run out of the box on any system with Python 3.

### How to Help Out

I'm doing some research on the properties of filesystems that grew out of a Computer Science 440 laboratory assignment. Over the course of the assignment, I realized that the filesystem on my computer is not perfectly generic, and that if I really want to know what filesystems tend to look like, I need a lot more data points. Therefore, I'd like to collect data from as diverse a selection of computers, operating systems, and usage patterns as possible. Here's where you come in.

If you want to help contribute to my filesystems statistics research project, please fork this repository, run `traverselite.py` on your home directory, create a CSV file, push your changes, and send me a pull request. I'm planning on doing all of my data analysis & graphing in an IPython notebook, which I'll make publicly available once it's complete.

If you're not familiar with how to fork and merge GitHub repositories, check out [this tutorial](http://guides.github.com/overviews/forking/).

`traverselite.py` should run on any computer with a working installation of Python 3 — Windows, Mac, Linux, it doesn't matter. Please collect data from as many computers as you can — your home computer, Alden Hall lab computers, et cetera. Traversal of extremely large filesystem trees may not happen instantaneously: I've seen traversals take as much as 15 seconds, so please give the script a few moments to run. It can be run in verbose mode, where it'll print every file and directory it encounters to the console, which can be used if you want to make sure the script is running and hasn't crashed.

The script will also collect a limited amount of metadata on runs (timestamp, traversal time, and operating system) and log them to `datafiles.csv` in the `data/` directory. If you're interested in seeing any of the eventual results of this study, or being credited in the event that this is ever published, please add your name and e-mail address to the CSV file. If you don't want to be contacted but you do be credited, just add your name and leave the email field blank. Thanks for helping out!

Usage instructions:
--------------------

```
Usage: 
    python traverselite.py (DIRECTORY) [--size] [--links] [--verbose] [--csv] [--nometadata]

Arguments:
    DIRECTORY           Root directory from which to begin traversal.

Options:
    --verbose       Verbose mode execution
    --size          Analyze file size
    --links         Analyze file link count
    --csv           Output a CSV
    --nometadata    Do not collect metadata on runs

```

If you want to contribute to my research, please run the following command from the repository root directory:
```
    python src/traverselite.py ~ --csv
```

Feel free to add the `--verbose`, `--size`, and `--links` flags as well, if you're interested in additional information. Do not enable the `--nometadata` flag if you want to contribute your data to my study.

Note also that `traverse.py` has a few additional options, which you can read about by running `traverse.py --help`.

Thanks guys!

 — Hawk (weismanm@allegheny.edu)
