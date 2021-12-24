# gds_1000b_scpi

## Introduction
[GDS-1000B](https://www.gwinstek.com/en-global/products/detail/GDS-1000B) series digital oscillocope by GW Instek is a cost effective instrument for engineers, technicians and students.  The oscilloscope includes a USB port for remote control.  Inside the oscilloscope there is a USB to serial converter.  An external computer opens this as a traditional serial port.

The instrument supports a reduced set of SCPI commands. SCPI is a general standard used by many equipment makers.  This python software tries to provide functions to work with the general SCPI command interface.  Some commands are unique to the GDS o-scope and these required special functions.

Python is used for engineering and science applications.  Jupyter Notebook and Spyder IDE are targeted at these users.  Functions in this repositiory are intended to work in Jupyter Notebook and other user friendly python environments.

The GDS oscillocopes have demo software available that uses Python.  See [OpenWave-1KB](https://github.com/OpenWave-GW/OpenWave-1KB) in Github.  Several forks exist.  OpenWave software has some limitations:

  * Originally written in python2, which is now obsolete.  This causes some dependency issues.  Some forks do upgrade the code to python 3
  * The OpenWave code is implemented as part of a Qt GUI demonstration.  The Qt GUI is more complex than needed. This doesn't really help with Jupyter Notebook.
  * The classes and methods are dependent on the GUI.  It is a challenge to reuse this code.
  * Serial communication to the instrument was not reliable on a Linux system.  The port would stop responding after 10-20 seconds of inactivity.  (I suspect this is a bug in the USB-serial conversion inside the instrument.)

The gds_1000b_scpi code is written in python3, functions are written to be independent where possible.  Concepts were borrowed from OpenWave, but nearly all was rewritten.

This is a work in progress.  Version 0.0 works in Jupyter Notebook, but just barely.  More work ahead.

## Files:
  * gds_scpi.py
      * functions to interact with GDS scope.  Import functions:  `from gds_scpi import function_name`
  * run_image_demo.py 
      * run the screen image demo from command line:  `python run_image_demo.py`
  * screen_image_demo.ipynb
      * Jupyter notebook page to show the screen image
  * run_acq_data_demo.py
      * run the demo to get waveform data, scale it and plot it
  * acquisition_data_demo.ipynb 
      * Jupyter notebook page to get, scale and plot waveform data
      * this uses inline plotting

## Speed
  * run_acq_data_demo.py was able to read and plot 100k points in 6 seconds
  * 1M point waveform took 22 seconds to read and plot
  * 10M point waveform took 2 min 55 seconds to read and plot
  * Most delay seems to be in getting raw data from the scope port.  It's not native USB, it's an emulated serial port.

## Dependencies

  * python 3.x
  * serial  >= ver 3.4
      * see [pyserial.readthedocs](https://pyserial.readthedocs.io/en/latest/)
  * pillow  8.x
      * see [pillow.readthedocs](https://pillow.readthedocs.io/en/stable/)
  * jupyter notebook ver 6.x
      * for ipynb support

## What's tested:

  * GDS-1202B scope with only 2 channels, BW 200MHz.  This unit does not have a network interface.  USB to serial port only.
  * Linux systems:  Manjaro (Arch based) and Sparky Linux (Debian based)
  * Python 3.8.x for now.  Now using Python 3.9.7
  * Jupyter Notebook and IPython kernel
  * Spyder 5

## Not tested:

  * Other GDS-1000B models, with 4 channels
  * Windows, Mac, RPi systems
      * Hope to try Raspberry Pi OS soon
  * Older python versions

