#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  gds_scpi.py
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

"""
Program name: gds_scpi.py
---------------------------------------------------
Description: 
- Control a GW Instek GDS-1000B series digital oscilloscope over USB serial.
- Based on OpenWave-1KB: https://github.com/OpenWave-GW/OpenWave-1KB.
- Remove the QT GUI code.
- Rewrite the major functions to make code blocks more independent and able
 to run in interactive environments like Jupyter notebook.
- Adjust serial port communication to work well in a Linux environment.
- This group of functions can:
    - Send general SCPI setting commands to the oscilloscope
    - Send general SCPI queries and get a response string
    - Use fixed SCPI query to get raw ADC data from acquisition memory
    - Use fixed SCPI query to get RLE encoded screen image
    - Convert RLE object to python image format for export and display
"""
import time
import serial
from PIL import Image

_VERSION_ = "0.0"

# ============================================================================
def scpi_query(cmd):
    ''' SCPI query: open port, send a query, get one line back, close port.
    Using pyserial context manager to open and close the port.
    Send characters very slowly for this type of query.  If not, the
    instrument won't reply. '''
    assert '?' in cmd, "Invalid SCPI query, must have question mark."
    assert cmd[0] in '*:', "Invalid SCPI query, must start with * or :"
    with ser as ser1:    # new context, opens port
        # send query command characters very slowly
        for str1 in cmd:
            ser1.write(str1.encode(encoding='ascii'))  # use 7-bit ASCII
            time.sleep(0.2)
        str2 = ser1.readline().decode()    # read response, UTF-8 is default
    return str2    # port now closed

# ============================================================================
def scpi_set(cmd):
    ''' SCPI set command: open port, send the command, close the port.
    Using pyserial context manager to open and close the port.
    include 100ms sleep for instrument processing '''
    assert not '?' in cmd, "Invalid SCPI set command, question mark found."
    assert cmd[0] in '*:', "Invalid SCPI query, must start with * or :"
    with ser as ser1:  # new context, opens port
        ser1.write(cmd.encode(encoding='ascii'))  # use 7-bit ASCII
        time.sleep(0.1)
    # port now closed

# ============================================================================
def scpi_acq_mem(chan):
    ''' SCPI acquisition memory query: open port, turn off header, send fixed
    query. Read and parse up to '#'. Get char count, get integer count,
    get large block of signed int16 data.  Then close port.
    Using pyserial context manager to open and close the port.
    Send characters very slowly for the query part. If not, the
    instrument won't reply.
    if channel number is invalid, instrument won't reply.
    returns a list of signed 8-bit ADC values, (-128...+127) in this case
    This function ignores the channel header. '''

    assert 1 <= chan <= 4, "Invalid channel number"
    # prepare command string
    cmd = ':ACQ' + str(int(chan)) + ':MEM?\n'

    with ser as ser1:    # new context, open port
        ser1.write(':HEAD OFF\n'.encode(encoding='ascii'))  # use 7-bit ASCII
        time.sleep(0.1)

        # send query command characters very slowly
        for str1 in cmd:
            ser1.write(str1.encode(encoding='ascii'))  # use 7-bit ASCII
            time.sleep(0.2)

        # read until '#' header identifier
        while ser1.read(1).decode() != '#':
            pass

        # get character count for numeric header
        char_count = int(ser1.read(1).decode())
        # get byte count number and divide by 2
        int_count = int(ser1.read(char_count).decode()) // 2

        # read a large list of signed integers
        raw_list = []
        for i in range(int_count):
            # read 2 bytes, convert to signed int
            val1 = int.from_bytes(
                ser1.read(2), byteorder='little', signed=True)
            raw_list.append(val1)
        # close port end of context
    return raw_list

# ============================================================================
def scpi_disp_out():
    ''' SCPI display output query: Get a copy of the display image.
    Open port, send fixed query.  Read and parse header up to '#'. Get char
    count, get int count, get RLE image as a large block of uint16 pairs.
    Then close port. Using pyserial context manager to open and close the
    port. Send characters very slowly for the query part.  If not, the
    instrument won't reply. '''

    # prepare command string
    CMD = ':DISP:OUTP?\n'

    with ser as ser1:    # new context, open port
        # send query command characters very slowly
        for str1 in CMD:
            ser1.write(str1.encode(encoding='ascii'))  # use 7-bit ASCII
            time.sleep(0.2)

        # read until '#' header identifier
        while ser1.read(1).decode() != '#':
            pass

        # get character count for numeric header
        char_count = int(ser1.read(1).decode())
        # get byte count number and divide by 4
        pixel_pairs = int(ser1.read(char_count).decode()) // 4
        # print('pixel bytes:', pixel_pairs*4)

        # read a large list of unsigned integer pairs
        # RLE encoding (pixel_count, pixel color)
        # no image decoding yet.
        rle_list = []
        for i in range(pixel_pairs):
            # convert 2 pairs of bytes to unsigned ints
            pixel_count = int.from_bytes(
                ser1.read(2), byteorder='little', signed=False)
            pixel_color = int.from_bytes(
                ser1.read(2), byteorder='little', signed=False)
            # build a list of RLE tuples (pixel count, pixel color)
            rle_list.append((pixel_count, pixel_color))

        ser1.flushInput()   # flush any remaining bytes
        # close port end of context
    return rle_list

# ============================================================================
def expand_rle(rle_thing):
    ''' Parse a big list of (count, pixel) tuples that represent RLE encoded
    screen image. Fixed 800x480 resolution.  Expand each run of pixels,
    rasterize, convert RGB565 color space, return an image object
    measured 186 ms per loop for a detailed test image '''

    assert type(rle_thing) == list, "RLE object isn't a list."

    # expand runs of pixels into a new list
    img_list = []
    for run_length, pixel_value in rle_thing:
        # each tuple is a run of same pixels, multiply repeated pixels
        img_list.extend([pixel_value] * run_length)

    # Constants for image size, color conversion
    WIDE = 800      # o-scope screen width
    HIGH = 480      # o-scope screen height
    RED_MASK = BLUE_MASK = 0xf8     # top 5 bits
    GREEN_MASK = 0xfc   # top 6 bits

    # instance of a new image with pixel access, 24 bit RGB mode
    im1 = Image.new('RGB', (WIDE, HIGH))
    pix_acc = im1.load()

    # list of pixels convert to raster
    for i, rgb_565 in enumerate(img_list):
        # calculate column (by modulo) and row (by int div)
        # byte align color bits, mask and merge
        pix_acc[i % WIDE, i // WIDE] = (rgb_565 >> 8 & RED_MASK,
                                        rgb_565 >> 3 & GREEN_MASK,
                                        rgb_565 << 3 & BLUE_MASK)

    # return the finished image
    return im1
# *** end ***
