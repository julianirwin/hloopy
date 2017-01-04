# -*- coding: utf-8 -*-
"""HLoopy CLI

Usage:
    hloopy.py --help
    hloopy.py COMMAND [options] PATH...

Arguments:
    COMMAND     Any one of [scmoke, arb, plot]
    PATH        Valid relative or absolute path.

Options:
    --help                     Print this message.
    -s --setas=XYSTRING        String that is used to determine the x and y 
                               data columns. If the file is four columns you
                               could use 'x..y' to set column 0 as the x column
                               and column 3 as the y column.
    -p --pattern=PATTERN       Regex used to select files to be plotted
                               [default: .*]
    -n --depth=INT             Number of levels down in the file tree to search
                               for data files when in 'plotarb' mode.
                               [default: 1]
    -o --output=FILENAME       Output filename. Output dir will be whatever
                               was passed to the '-d' switch.
                               [default: out.txt]
    -O --orientation=NESW      A string with some permutation of the characters
                               'NESW' (cardinal directions). The first two
                               characters specify the location of the origin
                               (0, 0) on the figure. For example, NE would
                               be the upper right. The third character is the
                               +x direction and the fourth character is the +y
                               direction. For example SENW means (0,0) is at
                               the lower right of the figure, (i, 0) is i
                               rows above (0, 0) and (0, j) is j columns to
                               the left of (0, 0).
                               [default: NWSE]
    --skiprows=INT             Number of lines to ignore in the datafile. 
                               Passed to pandas.read_csv
                               [default: 0]
    --seperator=CHAR           Seperator char in data file. Passed to 
                               pandas.read_csv
                               [default: \t]
    --smoothwidth=INT          Width parameter for the gaussian smoother.
                               [default: 20]
    --showaxes                 By default the axes around the loops are not
                               drawn. Pass this parameter to draw them.
    --verbose                  Print out more messages.
    --folderisid               Means that the directory of the data, not the
                               filename of the data has the identifying name.
                               For example, maybe data is stored in dirs with
                               the scheme `1000/, 1001/, ...` but each file
                               has the name `data.txt`. Then pass this argument
                               to see the folder name not `data.txt` in the
                               plot and parameters output file.
    

"""
import hloopy as hlpy
from hloopy.extract import Coercivity, Remanence, Saturation
from hloopy.plotters import GridPlot
from docopt import docopt
import re
import os
from os.path import join
import matplotlib.pyplot as plt

def arb(d):
    pass

def scmoke(d):
    scandir = d['PATH'][0]
    pat = '.*averaged.txt'
    datapaths = [join(scandir, f) for f in os.listdir(scandir) 
                 if re.match(pat, f)]
    hls = [hlpy.HLoop(f, sep='\t', skiprows=1) for f in datapaths]
    [hl.setas('x.y') for hl in hls]
    hideaxes = not d['--showaxes']
    lablevel = 1 if d['--folderisid'] else 0
    gp = GridPlot(hls, hideaxes=hideaxes, legend=True, lablevel=lablevel)
    gp.extract(Coercivity)
    gp.plot()
    plt.show()
    plt.close()

def plot(d):
    sep = d['--seperator']
    skiprows = d['--skiprows']
    hl = hlpy.HLoop(d['PATH'][0], sep=sep, skiprows=skiprows)
    hl.setas(d['--setas'])
    fig, ax = plt.subplots()
    hl.plot(ax)
    plt.show()

def main():
    d = docopt(__doc__)
    print(d)
    d['--skiprows'] = int(d['--skiprows'])
    commands = {
        'scmoke': scmoke, 
        'arb': arb,
        'plot': plot}
    commands[d['COMMAND'].lower()](d)
