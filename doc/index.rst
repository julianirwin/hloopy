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
   :maxdepth: 2

  hloopy


Examples
--------

This module is largely based on the familiar numpy, pandas and matplotlib
APIs we all know and love.

.. code-block::
  
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




Indices and tables
==================

* :ref:`modindex`
