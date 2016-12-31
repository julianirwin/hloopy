# -*- coding: utf-8 -*-
"""HLoopy CLI

Usage:
    hloopy.py --help
    hloopy.py sMOKE [--showaxes] [--verbose] [--orientation=NESW] PATH
    hloopy.py arb [options] PATH...

Arguments:
    COMMAND     Any one of [sMOKE, arb]
    PATH        Valid relative or absolute path.

Options:
    --help                     Print this message.
    -c --cols=TUPLE            Columns to read from data files. Of form (x,y).
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
from docopt import docopt

def main():
    d = docopt(__doc__)
    print(d)
