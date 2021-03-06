.. hloopy documentation master file, created by
   sphinx-quickstart on Mon Dec 12 17:53:32 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

HLoopy
======

Welcome to the documentation for HLoopy, a python module for analyzing 
hysteresis loop data. 

Contents

.. toctree::

  hloopy


Examples
--------

This module is largely based on the familiar numpy, pandas and matplotlib
APIs we all know and love.

.. code-block:: python

   import hloopy as hlpy
   # Here is a tsv datafile with 5 comment lines and 3 data columns
   datapath = 'path/to/some/data.txt'

   # Create an HLoop object, the wrapper around a datafile
   hl = hlpy.HLoop(datapath, sep='\t', skiprows=5)

   # Indicate which columns are the x and y data (stimulus and response).
   hl.setas(x=0, y=1)

   # Plotting the loop is easy:
   import matplotlib.pyplot as plt
   fig, ax = plt.subplots()
   # Plot, with a few special params. All axes.plot() kwargs are allowed.
   hl.plot(ax, ls='--', c='k')
   plt.show()
   plt.close()

   # Now compute the coercivity, remanence and saturation:
   from hlpy.extract import Coercivity, Remanence, Saturation
   fig, ax = plt.subplots()
   hl.plot(ax, ls='--', c='k')
   extracts = (Coercivity, Remanence, Saturation)
   for e in extracts:
       e(hl).plot(ax)
   plt.show()
   plt.close()

   # Use GridPlot() to plot many HLoops on a 2d-grid of axes
   # An arbitrary  number of extracts can be added to the plot.
   from hloopy.plotters import GridPlot
   hls = [HLoop(fpath) for fpath in fpath_list]
   gp = GridPlot(self.hls, hideaxes=True, legend=True)
   gp.extract(Coercivity, Remanence, Saturation)
   gp.plot()
   plt.close()


Custom Extracts
---------------

The easiest way to add an extract is to subclass :code:`hloolpy.ExtractBase`.
However, the only requirements for an extract are that it takes an
:code:`HLoopy.hloop` object when initialized (or called) and that the resulting
object has a :code:`.plot(ax, ...)` method.

Here is an example of a new extract that just finds the first point from the
HLoop and plots a marker there. See the source for the `Extract` submodule for
more complex examples.

.. code-block:: python

   from hloopy import HLoop
   from hloopy.extract import ExtractBase

   class VanillaExtract(ExtractBase):
       def __init__(self, hloop, setting=10):
           self.hloop = hloop
           self.setting = 10
       
       def plot(self, ax, **kwargs):
           style = {'linestyle': 'none', 'marker': 'o'}
           style.update(kwargs)
           xpoint = hloop.x()[0]
           ypoint = hloop.y()[0]
           ax.plot(xpoint, ypoint, **style)

Custom Data Preprocessing
-------------------------

As is, the :code:`hloopy.HLoop` module only allows the x and y data to 
be a column taken straight from a data file. Sometimes the need
arises to preprocess the data in some way, possibly merging 
two or more columns from the data file. A simple subclass 
of the :code:`HLoop` allows arbitrary preprocessing:

.. code-block:: python

   from hloopy import HLoop

   class CustomHLoop(HLoop):
       def x(self):
           return self.custom_preprocessing(self._x())
       
       def custom_preprocessing(self, arr):
           # Do some stuff to arr...
           return arr

Modifying the y preprocessing is exactly analogous. The :code:`HLoop._x()`
method is what the default :code:`x()` function calls to get the x axis data:
           
.. code-block:: python

   class HLoop:
       def x(self):
           return self._x()
       
       # (this is only a sketch of _x()...see code in hloop module)
       def _x(self):
           return self.df.ix[:, self.xcol]


Storing Frequently Used Custom Classes
--------------------------------------

(Not yet implemented)


Todo
----

  - CLI
    - arb function
  - Stoner model module
    - Have this code in modelplotlib
  - Write extracts to file.
    - Shorthand for mapping a bunch of extracts to a bunch of files
  - Extracts only plot.
    - Should take the output of a writer as it's input
  - pep8 everything
  - .config class files
  - Carefully avoid code that makes new copies of the columns
    in the original DataFrame.
  - Memoize HLoop.x(), HLoop.y(). Actually, not really memoize,
    maybe just compute them once upon initialization. But
    I did want to allow x()/y() to take parameters, and in that
    case memoization would be the right thing...
  - Gridplot NESW rotation of grid
    - Copy mostly from sMOKE
  - Fix Remanence extract. It's NaNing on the SOT data.
  - ExtractWRiter docstring
  - test on single column data
  - custom title functions for gridplot




Indices and tables
==================

* :ref:`modindex`
