# gds_1000b_scpi

# Introduction
GDS-1000B series digital oscillocope by GW Instek is a cost effective instrument for engineers, technicians and students.  The oscilloscope includes a USB port for remote control.  Inside the oscilloscope there is a USB to serial converter.  An external computer opens this as a traditional serial port.

The instrument supports a reduced set of SCPI commands. SCPI is a general standard used by many equipment makers.  This python software tries to provide functions to work with the general SCPI command interface.  Some commands are unique to the GDS o-scope and these required special functions.

Python is used for engineering and science applications.  Jupyter Notebook and Spyder IDE are targeted at these users.  Functions in this repositiory are intended to work in Jupyter Notebook and other user friendly python environments.

The GDS oscillocopes have demo software available that uses Python.  See OpenWave-1KB in Github.  Several forks exist.  OpenWave software has some limitations:

  * Originally written in python2, which is now obsolete.  This causes some dependency issues.  Some forks do upgrade the code to python 3
  * The OpenWave code is implemented as part of a Qt GUI demonstration.  The Qt GUI is more complex than needed. This doesn't really help with Jupyter Notebook.
  * The classes and methods are dependent on the GUI.  It is a challeng to reuse this code.
  * Serial communication to the instrument was not reliable on a Linux system.  The port would stop responding after 10-20 seconds of inactivity.  (I suspect this is a bug in the USB-serial conversion inside the instrument.)

The gds_1000b_scpi code is written in python3, functions are written to be independent where possible.  Concepts were borrowed from OpenWave, but nearly all was rewritten.

This is a work in progress.  Version 0.0 works in Jupyter Notebook, but just barely.  More work ahead.

What was tested:

  * GDS-1202B scope with only 2 channels at 200MHz.  This does not have a network interface.  USB to serial port only.
  * Linux computers:  Manjaro (Arch based) and Sparky Linux (Debian based)
  * Python 3.8.x for now
  * Jupyter Notebook and IPython kernel
  * Spyder 5

Not tested:

  * Other GDS-1000B models, with 4 channels
  * Windows, Mac, RPi systems
  * Older python versions

