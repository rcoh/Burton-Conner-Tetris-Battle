# util.py
# Copyright (C) 2011  Russell Cohen <rcoh@mit.edu>
#
# This file is part of Burton-Conner Tetris Battle.
#
# Burton-Conner Tetris Battle is free software: you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Burton-Conner Tetris Battle is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Burton-Conner Tetris Battle.  If not, see
# <http://www.gnu.org/licenses/>.

from numpy import zeros
from pygame import Color
import socket
import random
argDict = {'flags': 0, 'startcode': 0x0fff, 'pad':0}

# Allocate a buffer for transmitted packets and fill it with magic
# Only works for strips of 50 pixels
xmit = zeros(174, dtype='ubyte')
xmit[:8], xmit[20:25] = [4,1,220,74,1,0,8,1], [150,0,255,15,191]

def composePixelStripPacket(values, port):
  xmit[16], xmit[24:] = port, values.ravel()
  return xmit

def getConnectedSocket(ip,port):
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  try:
    sock.connect((ip, port))
    return sock
  except Exception as inst:
    print 'socket failure'

def shift_dict(shape_dict, change):
  return_dict = {}
  for (x,y) in shape_dict:
    return_dict[(x + change[0], y + change[1])] = shape_dict[(x, y)]
  return return_dict
def shift_dict_copy(initial_dict, change_rate, delta_time):
  """
  @param initial_dict -- the shape in "root position"
  @param change_rate -- the change rate in pixels / second as a tuple of (x,y)
  @param delta_time -- the time difference in seconds since 0 time
  """
  return_dict = {}
  delta_x, delta_y = change_rate
  for (x,y) in initial_dict:
    return_dict[(x + delta_x * delta_time, y + delta_y * delta_time)] = initial_dict[(x,y)]

  return return_dict

def compose_dicts(dict1, dict2, offset):
  result_dict = {}
  for key in dict1:
    result_dict[key] = dict1[key]

  for (x, y) in dict2:
    result_dict[(x + offset[0], y + offset[1])] = dict2[(x, y)]

  return result_dict

def twinkle(dict1):
  for key in dict1:
    if isinstance(dict1[key], str):
      dict1[key] = Color(dict1[key])[:3]
    r,g,b = dict1[key]
    dict1[key] = [r + random.randint(-5,5), g + random.randint(-5, 5), b + random.randint(-5, 5)]
    dict1[key] = safe_color(dict1[key])
  return dict1

def safe_color(c):
    """Ensures that a color is valid"""
    c[0] = c[0] if c[0] < 255 else 255
    c[1] = c[1] if c[1] < 255 else 255
    c[2] = c[2] if c[2] < 255 else 255
    return c

def get_dict_bounds(shape_dict):
  x_list = [loc[0] for loc in shape_dict.keys()]
  y_list = [loc[1] for loc in shape_dict.keys()]
  return min(x_list), max(x_list), min(y_list), max(y_list)
