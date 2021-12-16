#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  main.py
#  default file header
#  Copyright 2021 bob <bob@e6330>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import pickle
import serial
import gds_scpi

# ============================================================================
# MAIN HERE
# ============================================================================
if __name__ == '__main__':
    # Main. Run the o-scope interface demo.
    # FIXME add command line option parsing here

    # configure port instance, but don't auto-open
    ser = serial.Serial(None, baudrate=38400,
                        bytesize=8, parity ='N', stopbits=1,
                        xonxoff=False, dsrdtr=False, rtscts=False,
                        timeout=2)
    # FIXME use list_ports() in serial.tools for port selection
    # set a fixed port path for now
    PORT = '/dev/ttyACM0'
    # PORT = '/dev/ttyACM1'
    ser.port = PORT

    print('start testing')

    # try reading the screen image
    print('reading display image next')
    img_dat = scpi_disp_out()

    # save the RLE object for another day?
    resp_str = input("Overwrite RLE object as ./rle_out1 (y or n)?")
    if 'y' in resp_str.lower():
        with open('rle_out1', mode='wb') as file_handle:
            pickle.dump(img_dat, file_handle)
        print('done file write')

    # display screen image (in a new window)
    im1 = expand_rle(img_dat)
    im1.show()
# *** end ***

