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
import socket
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
